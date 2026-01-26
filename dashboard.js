// 테마 초기화 함수
function initializeTheme() {
  const getStoredTheme = () => localStorage.getItem("theme");
  const setStoredTheme = (theme) => localStorage.setItem("theme", theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  };

  const setTheme = (theme) => {
    if (theme === "auto") {
      document.documentElement.setAttribute(
        "data-bs-theme",
        window.matchMedia("(prefers-color-scheme: dark)").matches
          ? "dark"
          : "light",
      );
    } else {
      document.documentElement.setAttribute("data-bs-theme", theme);
    }
  };

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitcher = document.querySelector("#bd-theme");

    if (!themeSwitcher) {
      return;
    }

    const themeSwitcherText = document.querySelector("#bd-theme-text");
    const activeThemeIcon = document.querySelector(".theme-icon-active");
    const btnToActive = document.querySelector(
      `[data-bs-theme-value="${theme}"]`,
    );

    if (!btnToActive) {
      return;
    }

    document
      .querySelectorAll("[data-bs-theme-value]")
      .forEach((element) => {
        element.classList.remove("active");
        element.setAttribute("aria-pressed", "false");
      });

    btnToActive.classList.add("active");
    btnToActive.setAttribute("aria-pressed", "true");

    if (activeThemeIcon) {
      const themeIcons = {
        light: "☀️",
        dark: "🌙",
        auto: "🌓",
      };
      activeThemeIcon.textContent = themeIcons[theme] || "🌓";
    }

    const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`;
    themeSwitcher.setAttribute("aria-label", themeSwitcherLabel);

    if (focus) {
      themeSwitcher.focus();
    }
  };

  setTheme(getPreferredTheme());
  showActiveTheme(getPreferredTheme());

  document.querySelectorAll("[data-bs-theme-value]").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const theme = toggle.getAttribute("data-bs-theme-value");
      setStoredTheme(theme);
      setTheme(theme);
      showActiveTheme(theme, true);
    });
  });
}

const stripLiveReload = (html) => {
  // live-server 주석 시작부터 파일 끝까지 제거
  html = html.replace(/<!-- Code injected by live-server -->[\s\S]*$/g, "");
  
  // WebSocket 코드도 제거 (live-server 코드)
  html = html.replace(/if\s*\(\s*['"]WebSocket['"]\s+in\s+window\s*\)[\s\S]*$/g, "");
  
  return html.trim();
};

const loadFragment = (selector, url, callback) => {
  $.ajax({
    url: url,
    type: 'GET',
    dataType: 'html',
    success: function(data) {
      try {
        console.log(`Raw data from ${url}:`, data.substring(0, 200));
        const cleanedData = stripLiveReload(data);
        console.log(`Cleaned data from ${url}:`, cleanedData.substring(0, 200));
        if (cleanedData && cleanedData.length > 0) {
          let processedData = cleanedData;
          
          // selector가 sidebar인 경우, GitHub Pages 경로(/dev-tools/)에 맞게 조정
          if (selector === "#sidebar") {
            const currentPath = window.location.pathname;
            
            // GitHub Pages 배포 환경 감지 (/dev-tools/ 포함)
            if (currentPath.includes('/dev-tools/')) {
              processedData = cleanedData.replace(/href="\.\.\/\.\.\/tools\//g, 'href="/dev-tools/tools/')
                                          .replace(/data-tool="\.\.\/\.\.\/tools\//g, 'data-tool="/dev-tools/tools/');
            }
          }
          
          $(selector).html(processedData);
          console.log(`✓ Loaded: ${url}`);
          if (callback) callback();
        } else {
          console.warn(`⚠ Empty content after cleanup: ${url}`);
        }
      } catch(e) {
        console.error(`✗ Error processing ${url}:`, e);
        console.error(`Raw data was:`, data);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.error(`✗ Failed to load ${url}:`, textStatus, errorThrown);
    }
  });
};
