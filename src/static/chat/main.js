/* ======================= THEME TOGGLE ======================= */
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;
const savedTheme = localStorage.getItem("theme") || "light";

if (savedTheme === "dark") {
  body.classList.add("dark-theme");
  updateThemeIcon(true);
}

themeToggle.addEventListener("click", () => {
  const isDark = body.classList.toggle("dark-theme");
  localStorage.setItem("theme", isDark ? "dark" : "light");
  updateThemeIcon(isDark);
});

function updateThemeIcon(isDark) {
  themeToggle.innerHTML = isDark
    ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>`
    : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>`;
}

/* ======================= SIDEBAR MENU ======================= */
const mobileMenuBtn = document.getElementById("mobile-menu-btn");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");

mobileMenuBtn?.addEventListener("click", () => {
  sidebar.classList.add("show");
  sidebarOverlay.classList.add("show");
});
sidebarOverlay.addEventListener("click", () => {
  sidebar.classList.remove("show");
  sidebarOverlay.classList.remove("show");
});

/* ======================= CHAT VARIABLES ======================= */
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const messagesContainer = document.getElementById("messages-container");
const welcomeScreen = document.getElementById("welcome-screen");
const chatContainer = document.getElementById("chat-container");

const attachFileBtn = document.getElementById("attach-file");
const fileInput = document.getElementById("file-input");
const attachedFileDiv = document.getElementById("attached-file");
const fileNameSpan = document.getElementById("file-name");
const removeFileBtn = document.getElementById("remove-file");

let attachedFile = null;
let conversations = JSON.parse(localStorage.getItem("conversations") || "[]");
let currentConversationId = null;

/* ======================= INPUT BEHAVIOR ======================= */
messageInput.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 120) + "px";
});

document.querySelectorAll(".quick-action").forEach((action) => {
  action.addEventListener("click", () => {
    const prompt = action.dataset.prompt;
    messageInput.value = prompt;
    messageInput.focus();
  });
});

attachFileBtn.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    attachedFile = file;
    fileNameSpan.textContent = file.name;
    attachedFileDiv.style.display = "flex";
  }
});
removeFileBtn.addEventListener("click", () => {
  attachedFile = null;
  fileInput.value = "";
  attachedFileDiv.style.display = "none";
});

/* ======================= SEND MESSAGE ======================= */
async function sendMessage() {
  let message = messageInput.value.trim();
  if (!message && !attachedFile) return;

  welcomeScreen.style.display = "none";
  messagesContainer.style.display = "block";

  if (!currentConversationId) {
    currentConversationId = Date.now().toString();
    conversations.unshift({
      id: currentConversationId,
      title: message.slice(0, 50) + (message.length > 50 ? "..." : ""),
      messages: [],
      timestamp: Date.now(),
    });
    updateConversationList();
  }

  const formData = new FormData();
  messageInput.value = "";
  messageInput.style.height = "auto";

  if (attachedFile) {
    formData.append("file", attachedFile);
    message = `${attachedFile.name}\n\n` + message;
  }
  if (message) formData.append("message", message);

  if (message) {
    displayMessage(message, "user");
    addMessageToConversation(currentConversationId, { role: "user", content: message });
  }

  attachedFile = null;
  attachedFileDiv.style.display = "none";
  fileInput.value = "";

  sendButton.disabled = true;
  sendButton.style.opacity = "0.6";

  showTypingIndicator();

  let assistantMessageElement = createMessageElement("", "assistant");
  messagesContainer.appendChild(assistantMessageElement);
  let assistantMessageContent = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      credentials: "include",
      body: formData,
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === "chunk" && data.content) {
              assistantMessageContent += data.content;
              updateMessageContent(assistantMessageElement, assistantMessageContent);
              chatContainer.scrollTop = chatContainer.scrollHeight;
            } else if (data.type === "done") {
              updateMessageContent(assistantMessageElement, assistantMessageContent);
            } else if (data.type === "error") {
              throw new Error(data.message);
            }
          } catch (err) {
            console.warn("Parse SSE error:", line, err);
          }
        }
      }
    }

    if (assistantMessageContent) {
      addMessageToConversation(currentConversationId, {
        role: "assistant",
        content: assistantMessageContent,
      });
    }
  } catch (error) {
    console.error("Streaming error:", error);
    hideTypingIndicator();
    assistantMessageElement.remove();
    displayMessage("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.", "assistant");
  } finally {
    hideTypingIndicator();
    addCopyButtons();
    sendButton.disabled = false;
    sendButton.style.opacity = "1";
    localStorage.setItem("conversations", JSON.stringify(conversations));
  }
}

/* ======================= MESSAGE ELEMENTS ======================= */
function createMessageElement(content, role) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const msg = document.createElement("div");
  msg.className = "message-content";
  if (content) msg.innerHTML = renderMessage(content);
  div.appendChild(msg);
  return div;
}

function updateMessageContent(element, content) {
  const msg = element.querySelector(".message-content");
  if (msg) msg.innerHTML = renderMessage(content);
}

function displayMessage(content, role) {
  const element = createMessageElement(content, role);
  messagesContainer.appendChild(element);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/* ======================= CONVERSATIONS ======================= */
function addMessageToConversation(conversationId, message) {
  const conv = conversations.find((c) => c.id === conversationId);
  if (conv) {
    conv.messages.push(message);
    conv.timestamp = Date.now();
  }
}
function updateConversationList() {
  const list = document.getElementById("conversation-list");
  list.innerHTML = "";
  conversations.forEach((conv) => {
    const item = document.createElement("div");
    item.className = "conversation-item" + (conv.id === currentConversationId ? " active" : "");
    item.textContent = conv.title;
    item.addEventListener("click", () => loadConversation(conv.id));
    list.appendChild(item);
  });
}
function loadConversation(id) {
  const conv = conversations.find((c) => c.id === id);
  if (!conv) return;
  currentConversationId = id;
  welcomeScreen.style.display = "none";
  messagesContainer.style.display = "block";
  messagesContainer.innerHTML = "";
  conv.messages.forEach((m) => displayMessage(m.content, m.role));
  updateConversationList();
  sidebar.classList.remove("show");
  sidebarOverlay.classList.remove("show");
}
function startNewConversation() {
  currentConversationId = null;
  welcomeScreen.style.display = "flex";
  messagesContainer.style.display = "none";
  messagesContainer.innerHTML = "";
  updateConversationList();
  sidebar.classList.remove("show");
  sidebarOverlay.classList.remove("show");
}
function removeOldConversations() {
  const now = Date.now();
  const oneDay = 24 * 60 * 60 * 1000;
  conversations = conversations.filter((c) => now - c.timestamp < oneDay);
  if (currentConversationId && !conversations.find((c) => c.id === currentConversationId)) {
    startNewConversation();
  }
  updateConversationList();
}

/* ======================= RENDER MESSAGE ======================= */
function renderMessage(content) {
  if (!content) return "";
  const codeBlocks = {};
  let text = preserveCodeBlocks(content, codeBlocks);
  text = escapeHtml(text);
  text = renderInlineCode(text);
  text = renderHeadings(text);
  text = renderTextStyles(text);
  text = renderLinksAndImages(text);
  text = renderBlockquotes(text);
  text = renderHorizontalRules(text);
  text = renderTaskLists(text);
  text = renderLists(text);
  text = renderTables(text);
  text = renderMath(text);
  text = restoreCodeBlocks(text, codeBlocks);
  text = optimizeLineBreaks(text);
  return text.trim();
}

/* ======================= HELPERS ======================= */
function preserveCodeBlocks(text, storage) {
  return text.replace(/```(\w+)?\s*\n?([\s\S]*?)```/g, (m, lang, code) => {
    const id = `CODEBLOCK_${Math.random().toString(36).slice(2, 9)}`;
    storage[id] = `<pre><code class="language-${lang || "text"}">${escapeHtml(code.trim())}</code></pre>`;
    return id;
  });
}
function restoreCodeBlocks(text, storage) {
  for (const id in storage) {
    text = text.replace(new RegExp(id, "g"), storage[id]);
  }
  return text;
}
function escapeHtml(text) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}
function renderInlineCode(text) {
  return text.replace(/`([^`\n]+)`/g, "<code>$1</code>");
}
function renderHeadings(text) {
  return text
    .replace(/^###### (.*)$/gm, "<h6>$1</h6>")
    .replace(/^##### (.*)$/gm, "<h5>$1</h5>")
    .replace(/^#### (.*)$/gm, "<h4>$1</h4>")
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, "<h1>$1</h1>");
}
function renderTextStyles(text) {
  return text
    .replace(/\*\*\*(.*?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/__(.*?)__/g, "<strong>$1</strong>")
    .replace(/_(.*?)_/g, "<em>$1</em>")
    .replace(/~~(.*?)~~/g, "<del>$1</del>");
}
function renderLinksAndImages(text) {
  return text
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/(https?:\/\/[^\s<>"]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width:100%;height:auto;">');
}
function renderBlockquotes(text) {
  return text.replace(/^>\s?(.*)$/gm, "<blockquote>$1</blockquote>");
}
function renderHorizontalRules(text) {
  return text.replace(/^(---|___|\*\*\*)$/gm, "<hr>");
}
function renderTaskLists(text) {
  return text.replace(/^[-*+] \[([ xX])\] (.*)$/gm, (m, check, item) => {
    const checked = check.toLowerCase() === "x" ? "checked" : "";
    return `<div class="task-item"><input type="checkbox" disabled ${checked}> ${item}</div>`;
  });
}
function renderLists(text) {
  const lines = text.split("\n");
  const result = [];
  const stack = [];
  function close(toLevel) {
    while (stack.length > toLevel) {
      const list = stack.pop();
      result.push(list.type === "ul" ? "</ul>" : "</ol>");
    }
  }
  for (let line of lines) {
    const ordered = line.match(/^(\s*)(\d+)\.\s+(.+)$/);
    const unordered = line.match(/^(\s*)[-*+]\s+(.+)$/);
    if (ordered || unordered) {
      const indent = (ordered ? ordered[1] : unordered[1]).length;
      const level = Math.floor(indent / 2);
      const type = ordered ? "ol" : "ul";
      const content = ordered ? ordered[3] : unordered[2];
      if (!stack.length || stack[stack.length - 1].type !== type || stack[stack.length - 1].level < level) {
        result.push(type === "ol" ? "<ol>" : "<ul>");
        stack.push({ type, level });
      } else if (stack[stack.length - 1].level > level) {
        close(level);
      }
      result.push(`<li>${content.trim()}</li>`);
    } else {
      close(0);
      result.push(line);
    }
  }
  close(0);
  return result.join("\n");
}
function renderTables(text) {
  const lines = text.split("\n");
  const result = [];
  let inTable = false;
  let isHeader = true;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) {
      if (inTable) {
        result.push("</tbody></table>");
        inTable = false;
      }
      result.push("");
      continue;
    }
    if (line.includes("|") && line.split("|").length >= 3) {
      const cells = line.split("|").map((c) => c.trim()).filter(Boolean);
      const next = lines[i + 1]?.trim();
      const isSeparator = next && /^[-:| ]+$/.test(next);
      if (!inTable) {
        result.push('<table class="markdown-table"><tbody>');
        inTable = true;
        isHeader = true;
      }
      if (isHeader && isSeparator) {
        result.push("<thead><tr>");
        cells.forEach((c) => result.push(`<th>${c}</th>`));
        result.push("</tr></thead><tbody>");
        isHeader = false;
        i++;
      } else {
        result.push("<tr>");
        cells.forEach((c) => result.push(`<td>${c}</td>`));
        result.push("</tr>");
      }
    } else {
      if (inTable) {
        result.push("</tbody></table>");
        inTable = false;
      }
      result.push(line);
    }
  }
  if (inTable) result.push("</tbody></table>");
  return result.join("\n");
}
function renderMath(text) {
  if (typeof katex === "undefined") return text;
  const safeRender = (math, display) => {
    try {
      return katex.renderToString(math.trim(), { displayMode: display, throwOnError: false, output: "html" });
    } catch {
      return `<span class="math-error">${math.trim()}</span>`;
    }
  };
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, m) => `<div class="katex-block">${safeRender(m, true)}</div>`);
  text = text.replace(/(?<!\$)\$([^$\n]+?)\$(?!\$)/g, (_, m) => `<span class="katex-inline">${safeRender(m, false)}</span>`);
  return text;
}
function optimizeLineBreaks(text) {
  return text.replace(/\n+/g, "<br>").replace(/(<br>\s*){3,}/g, "<br><br>");
}

/* ======================= TYPING INDICATOR ======================= */
function showTypingIndicator() {
  const div = document.createElement("div");
  div.className = "typing-indicator";
  div.id = "typing-indicator";
  div.innerHTML = `<div class="typing-dots">
    <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
  </div>`;
  messagesContainer.appendChild(div);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
function hideTypingIndicator() {
  document.getElementById("typing-indicator")?.remove();
}

/* ======================= COPY BUTTONS ======================= */
function addCopyButtons() {
  const blocks = document.querySelectorAll(".message-content pre");
  blocks.forEach((block) => {
    if (block.parentElement.classList.contains("code-block-wrapper")) return;
    const wrapper = document.createElement("div");
    wrapper.className = "code-block-wrapper";
    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-button";
    copyBtn.textContent = "Copy";
    copyBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(block.innerText);
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy"), 2000);
      } catch {
        console.error("Copy failed");
      }
    });
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(copyBtn);
    wrapper.appendChild(block);
  });
}

/* ======================= INIT ======================= */
removeOldConversations();
sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
document.getElementById("new-chat-btn").addEventListener("click", startNewConversation);
updateConversationList();
messageInput.focus();

document.getElementById("voice-input").addEventListener("click", () => {
  alert("Tính năng ghi âm sẽ được phát triển trong tương lai!");
});

/* ======================= UTILITIES ======================= */
function setViewportHeight() {
  document.documentElement.style.setProperty("--vh", `${window.innerHeight * 0.01}px`);
}
setViewportHeight();
window.addEventListener("resize", setViewportHeight);
window.addEventListener("orientationchange", () => setTimeout(setViewportHeight, 500));

if (window.innerWidth <= 768) {
  messageInput.addEventListener("focus", () => {
    setTimeout(() => {
      messageInput.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 300);
  });
}
document.getElementById("logout-btn").addEventListener("click", () => (window.location.href = "/logout"));
function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
