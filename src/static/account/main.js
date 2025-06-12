let accessToken = null;

async function loginWithGoogle() {
  const btn = document.getElementById("loginBtn");
  const loading = document.getElementById("loading");

  btn.style.transform = "scale(0.95)";

  setTimeout(() => {
    btn.style.display = "none";
    loading.classList.add("show");
  }, 200);

  setTimeout(() => {
    window.location.href = "/login/google";
  }, 1500);
}

window.onload = () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");
  const statusEl = document.getElementById("status");

  if (token) {
    accessToken = token;

    statusEl.innerHTML =
      "🚀 Đăng nhập thành công! Chào mừng bạn đến với hệ thống.";
    statusEl.classList.add("success", "show");

    document.getElementById("loginBtn").style.display = "none";
    document.getElementById("loading").classList.remove("show");

    console.log("Token được lưu:", accessToken);

    createConfetti();
  }
};

function createConfetti() {
  const colors = ["#4285f4", "#ea4335", "#fbbc05", "#34a853"];

  for (let i = 0; i < 50; i++) {
    const confetti = document.createElement("div");
    confetti.style.position = "absolute";
    confetti.style.width = "10px";
    confetti.style.height = "10px";
    confetti.style.backgroundColor =
      colors[Math.floor(Math.random() * colors.length)];
    confetti.style.left = Math.random() * 100 + "%";
    confetti.style.animationDuration = Math.random() * 3 + 2 + "s";
    confetti.style.animationName = "confettiFall";
    confetti.style.zIndex = "1000";

    document.body.appendChild(confetti);

    setTimeout(() => {
      confetti.remove();
    }, 5000);
  }
}

const style = document.createElement("style");
style.textContent = `
      @keyframes confettiFall {
          0% {
              transform: translateY(-100vh) rotate(0deg);
              opacity: 1;
          }
          100% {
              transform: translateY(100vh) rotate(720deg);
              opacity: 0;
          }
      }
  `;

document.head.appendChild(style);
const loginBtn = document.getElementById("loginBtn");
loginBtn.addEventListener("click", () => {
  window.location.href = "/login/google";
});
