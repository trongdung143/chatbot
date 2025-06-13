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

attachFileBtn.addEventListener("click", () => {
  fileInput.click();
});

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

async function sendMessage() {
  let message = messageInput.value.trim();

  if (!message && !attachedFile) return;

  welcomeScreen.style.display = "none";
  messagesContainer.style.display = "block";

  if (!currentConversationId) {
    currentConversationId = Date.now().toString();
    const newConversation = {
      id: currentConversationId,
      title: message.slice(0, 50) + (message.length > 50 ? "..." : ""),
      messages: [],
      timestamp: Date.now(),
    };
    conversations.unshift(newConversation);
    updateConversationList();
  }

  const formData = new FormData();

  messageInput.value = "";
  messageInput.style.height = "auto";

  if (attachedFile) {
    formData.append("file", attachedFile);
    message = `${attachedFile.name}\n\n` + message;
  }

  if (message) {
    formData.append("message", message);
  }

  if (message) {
    displayMessage(message, "user");
    addMessageToConversation(currentConversationId, {
      role: "user",
      content: message,
    });
  }

  attachedFile = null;
  attachedFileDiv.style.display = "none";
  fileInput.value = "";

  sendButton.disabled = true;
  sendButton.style.opacity = "0.6";

  showTypingIndicator();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      credentials: "include",
      body: formData,
    });

    sendButton.disabled = false;
    sendButton.style.opacity = "1";
    hideTypingIndicator();

    const data = await response.json();
    displayMessage(data.response, "assistant");
    addMessageToConversation(currentConversationId, {
      role: "assistant",
      content: data.response,
    });
  } catch (error) {
    sendButton.disabled = false;
    sendButton.style.opacity = "1";
    hideTypingIndicator();

    displayMessage("Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.", "assistant");
  }

  localStorage.setItem("conversations", JSON.stringify(conversations));
}

function formatMessage(text) {
  if (!text) return "";

  // Lưu trữ code blocks để bảo vệ khỏi escape HTML
  const codeBlocks = {};

  // Xử lý code blocks TRƯỚC khi escape HTML
  text = text.replace(/```(\w+)?\s*\n?([\s\S]*?)```/g, (match, lang, code) => {
    // Tạo placeholder an toàn (không chứa ký tự đặc biệt)
    const placeholder = `CODEBLOCK${Math.random()
      .toString(36)
      .substr(2, 9)}PLACEHOLDER`;
    const codeBlock = `<pre><code class="language-${
      lang || "text"
    }">${code.trim()}</code></pre>`;
    // Lưu mapping để restore sau
    codeBlocks[placeholder] = codeBlock;
    return placeholder;
  });

  // Escape HTML (nhưng không ảnh hưởng code blocks)
  text = escapeHtml(text);

  // Inline code
  text = text.replace(/`([^`\n]+)`/g, "<code>$1</code>");

  // Headers
  text = text
    .replace(/^#{6}\s+(.+)$/gm, "<h6>$1</h6>")
    .replace(/^#{5}\s+(.+)$/gm, "<h5>$1</h5>")
    .replace(/^#{4}\s+(.+)$/gm, "<h4>$1</h4>")
    .replace(/^#{3}\s+(.+)$/gm, "<h3>$1</h3>")
    .replace(/^#{2}\s+(.+)$/gm, "<h2>$1</h2>")
    .replace(/^#{1}\s+(.+)$/gm, "<h1>$1</h1>");

  // Bold, italic, strikethrough
  text = text
    .replace(/\*\*\*(.*?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/__(.*?)__/g, "<strong>$1</strong>")
    .replace(/_(.*?)_/g, "<em>$1</em>");

  text = text.replace(/~~(.*?)~~/g, "<del>$1</del>");

  // [download/chapter1.pdf] => <a href="..." target>chapter1.pdf</a>
  text = text.replace(
    /\[([^\]]+\.(pdf|docx?|xlsx?|zip|rar))\]/gi,
    (_, fullPath) => {
      const fileName = fullPath.split("/").pop();
      return `<a href="${fullPath}" target="_blank" rel="noopener noreferrer">${fileName}</a>`;
    }
  );

  // [Text](URL) Markdown => liên kết
  text = text.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
  );

  // URL thuần => liên kết
  text = text.replace(
    /(https?:\/\/[^\s<>"]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  );

  // Images
  text = text.replace(
    /!\[([^\]]*)\]\(([^)]+)\)/g,
    '<img src="$2" alt="$1" style="max-width: 100%; height: auto;">'
  );

  // Blockquotes
  text = text.replace(/^>\s*(.*)$/gm, "<blockquote>$1</blockquote>");
  text = text.replace(/<\/blockquote>\s*<blockquote>/g, "<br>");

  // Horizontal rules
  text = text.replace(/^(---|___|\*\*\*)\s*$/gm, "<hr>");

  // Lists và Tables
  text = formatLists(text);
  text = formatTables(text);
  text = renderMath(text);

  // Restore code blocks từ placeholders (QUAN TRỌNG: phải làm TRƯỚC khi xử lý line breaks)
  Object.keys(codeBlocks).forEach((placeholder) => {
    text = text.replace(new RegExp(placeholder, "g"), codeBlocks[placeholder]);
  });

  // XỬ LÝ KHOẢNG TRẮNG VÀ LINE BREAKS CẢI THIỆN
  // Loại bỏ khoảng trắng thừa ở đầu/cuối mỗi dòng
  text = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line, index, arr) => {
      // Giữ lại dòng trống nhưng không quá 2 dòng liên tiếp
      if (line === "") {
        const prevEmpty = index > 0 && arr[index - 1] === "";
        const nextEmpty = index < arr.length - 1 && arr[index + 1] === "";
        return !(prevEmpty && nextEmpty);
      }
      return true;
    })
    .join("\n");

  // Xử lý các trường hợp đặc biệt cho HTML tags
  text = text.replace(/>\s*<br>\s*</g, "><"); // Loại bỏ <br> giữa các tags
  text = text.replace(/<\/(\w+)>\s*<br>\s*<(\w+)>/g, "</$1><$2>"); // Loại bỏ <br> giữa closing và opening tags

  // Chuyển newlines thành <br>, nhưng không ảnh hưởng đến HTML structure
  text = text.replace(/\n(?!<)/g, "<br>"); // Chỉ thay \n không phải trước HTML tags

  // Làm sạch <br> thừa
  text = text.replace(/(<br>\s*){3,}/g, "<br><br>"); // Tối đa 2 <br> liên tiếp
  text = text.replace(/\s*<br>\s*/g, "<br>"); // Loại bỏ spaces xung quanh <br>

  return text.trim();
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

function formatLists(text) {
  const lines = text.split("\n");
  const result = [];
  const stack = [];

  function closeLists(toLevel) {
    while (stack.length > toLevel) {
      const list = stack.pop();
      result.push(list.type === "ul" ? "</ul>" : "</ol>");
    }
  }

  for (let line of lines) {
    // Trim line để xử lý khoảng trắng
    const trimmedLine = line.trim();

    const orderedMatch = line.match(/^(\s*)(\d+)\.\s+(.+)$/);
    const unorderedMatch = line.match(/^(\s*)[-*+]\s+(.+)$/);

    if (orderedMatch) {
      const indent = orderedMatch[1].length;
      const level = Math.floor(indent / 2);
      const content = orderedMatch[3].trim(); // Trim content

      if (
        stack.length === 0 ||
        stack[stack.length - 1].type !== "ol" ||
        stack[stack.length - 1].level < level
      ) {
        result.push("<ol>");
        stack.push({ type: "ol", level });
      } else if (stack[stack.length - 1].level > level) {
        closeLists(level);
      } else if (stack[stack.length - 1].type !== "ol") {
        closeLists(level);
        result.push("<ol>");
        stack.push({ type: "ol", level });
      }

      result.push(`<li>${content}</li>`);
      continue;
    }

    if (unorderedMatch) {
      const indent = unorderedMatch[1].length;
      const level = Math.floor(indent / 2);
      const content = unorderedMatch[2].trim(); // Trim content

      if (
        stack.length === 0 ||
        stack[stack.length - 1].type !== "ul" ||
        stack[stack.length - 1].level < level
      ) {
        result.push("<ul>");
        stack.push({ type: "ul", level });
      } else if (stack[stack.length - 1].level > level) {
        closeLists(level);
      } else if (stack[stack.length - 1].type !== "ul") {
        closeLists(level);
        result.push("<ul>");
        stack.push({ type: "ul", level });
      }

      result.push(`<li>${content}</li>`);
      continue;
    }

    closeLists(0);
    result.push(trimmedLine); // Sử dụng trimmed line
  }

  closeLists(0);
  return result.join("\n");
}

function formatTables(text) {
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
      result.push(""); // Giữ dòng trống
      continue;
    }

    if (line.includes("|") && line.split("|").length >= 3) {
      const cells = line
        .split("|")
        .map((cell) => cell.trim())
        .filter((cell) => cell.length > 0);

      const nextLine = i + 1 < lines.length ? lines[i + 1].trim() : "";
      const isSeparator = nextLine && /^\|?[\s\-:|]+\|?$/.test(nextLine);

      if (!inTable) {
        result.push(
          '<table border="1" style="border-collapse: collapse; margin: 10px 0;">'
        );
        inTable = true;
        isHeader = true;
      }

      if (isHeader && isSeparator) {
        result.push("<thead><tr>");
        cells.forEach((cell) => {
          result.push(
            `<th style="padding: 8px; background-color: #f5f5f5;">${cell}</th>`
          );
        });
        result.push("</tr></thead><tbody>");
        isHeader = false;
        i++; // Skip separator line
      } else {
        if (isHeader) {
          result.push("<thead><tr>");
          cells.forEach((cell) => {
            result.push(
              `<th style="padding: 8px; background-color: #f5f5f5;">${cell}</th>`
            );
          });
          result.push("</tr></thead><tbody>");
          isHeader = false;
        } else {
          result.push("<tr>");
          cells.forEach((cell) => {
            result.push(`<td style="padding: 8px;">${cell}</td>`);
          });
          result.push("</tr>");
        }
      }
    } else {
      if (inTable) {
        result.push("</tbody></table>");
        inTable = false;
      }
      result.push(line);
    }
  }

  if (inTable) {
    result.push("</tbody></table>");
  }

  return result.join("\n");
}

function renderMath(text) {
  if (typeof katex !== "undefined") {
    // Display math ($$...$$)
    text = text.replace(/\$\$([^$]+)\$\$/g, (match, math) => {
      try {
        return katex.renderToString(math.trim(), { displayMode: true });
      } catch (e) {
        console.warn("KaTeX render error:", e);
        return `<span class="math-error">${escapeHtml(math.trim())}</span>`;
      }
    });

    // Inline math ($...$)
    text = text.replace(/\$([^$]+)\$/g, (match, math) => {
      try {
        return katex.renderToString(math.trim(), { displayMode: false });
      } catch (e) {
        console.warn("KaTeX render error:", e);
        return `<span class="math-error">${escapeHtml(math.trim())}</span>`;
      }
    });
  }
  return text;
}

function showTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.className = "typing-indicator";
  typingDiv.id = "typing-indicator";

  const dotsDiv = document.createElement("div");
  dotsDiv.className = "typing-dots";
  dotsDiv.innerHTML =
    '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

  typingDiv.appendChild(dotsDiv);

  messagesContainer.appendChild(typingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) {
    indicator.remove();
  }
}

function addMessageToConversation(conversationId, message) {
  const conversation = conversations.find((c) => c.id === conversationId);
  if (conversation) {
    conversation.messages.push(message);
    conversation.timestamp = Date.now();
  }
}

function updateConversationList() {
  const listContainer = document.getElementById("conversation-list");
  listContainer.innerHTML = "";

  conversations.forEach((conversation) => {
    const item = document.createElement("div");
    item.className = "conversation-item";
    if (conversation.id === currentConversationId) {
      item.classList.add("active");
    }
    item.textContent = conversation.title;
    item.addEventListener("click", () => loadConversation(conversation.id));
    listContainer.appendChild(item);
  });
}

function displayMessage(content, sender) {
  if (!messagesContainer) {
    console.error("Messages container not found!");
    return;
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const messageContent = document.createElement("div");
  messageContent.className = "message-content";

  const formatted = formatMessage(content);
  messageContent.innerHTML = formatted;

  messageDiv.appendChild(messageContent);
  messagesContainer.appendChild(messageDiv);

  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function loadConversation(conversationId) {
  const conversation = conversations.find((c) => c.id === conversationId);
  if (!conversation) return;

  currentConversationId = conversationId;
  welcomeScreen.style.display = "none";
  messagesContainer.style.display = "block";
  messagesContainer.innerHTML = "";

  conversation.messages.forEach((message) => {
    displayMessage(message.content, message.role);
  });

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
  const oneDay = 24 * 60 * 60;
  conversations = conversations.filter((conversation) => {
    return now - conversation.timestamp < oneDay;
  });

  if (
    currentConversationId &&
    !conversations.find((c) => c.id === currentConversationId)
  ) {
    startNewConversation();
  }

  updateConversationList();
}

removeOldConversations();

sendButton.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

document
  .getElementById("new-chat-btn")
  .addEventListener("click", startNewConversation);

updateConversationList();

messageInput.focus();

document.getElementById("voice-input").addEventListener("click", () => {
  alert("Tính năng ghi âm sẽ được phát triển trong tương lai!");
});

function setViewportHeight() {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty("--vh", `${vh}px`);
}

setViewportHeight();
window.addEventListener("resize", setViewportHeight);
window.addEventListener("orientationchange", () => {
  setTimeout(setViewportHeight, 500);
});

if (window.innerWidth <= 768) {
  messageInput.addEventListener("focus", () => {
    setTimeout(() => {
      messageInput.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }, 300);
  });
}
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll(".message-content pre");

  codeBlocks.forEach((block) => {
    if (block.parentElement.classList.contains("code-block-wrapper")) return;

    const wrapper = document.createElement("div");
    wrapper.className = "code-block-wrapper";

    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-button";
    copyBtn.textContent = "copy";

    copyBtn.addEventListener("click", () => {
      const codeText = block.textContent;
      navigator.clipboard
        .writeText(codeText)
        .then(() => {
          copyBtn.textContent = "copied";
          copyBtn.classList.add("copied");
          setTimeout(() => {
            copyBtn.textContent = "copy";
            copyBtn.classList.remove("copied");
          }, 2000);
        })
        .catch((err) => {
          console.error("Lỗi khi sao chép:", err);
        });
    });

    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(copyBtn);
    wrapper.appendChild(block);
  });
}

const originalDisplayMessage = displayMessage;
displayMessage = function (content, sender) {
  originalDisplayMessage(content, sender);
  addCopyButtons();
};

const logOut = document.getElementById("logout-btn");
logOut.addEventListener("click", () => {
  window.location.href = "/logout";
});
