
                let newsData = [];
                let currentSlideIndex = 0;
                const itemsPerSlide = 3;

                // hn.json에서 데이터 로드
                fetch("/dev-tools/python_job/data/hn.json")
                  .then((response) => response.json())
                  .then((data) => {
                    newsData = data;
                    if (newsData && newsData.length > 0) {
                      renderNewsSlides();
                      updateSlideDisplay();
                      document.getElementById("newsSection").style.display =
                        "block";
                    }
                  })
                  .catch((error) => console.log("News data not available"));

                function timestampToLocalDateTime(timestamp) {
                  const date = new Date(timestamp * 1000);
                  const year = date.getFullYear();
                  const month = String(date.getMonth() + 1).padStart(2, "0");
                  const day = String(date.getDate()).padStart(2, "0");
                  const hours = String(date.getHours()).padStart(2, "0");
                  const minutes = String(date.getMinutes()).padStart(2, "0");
                  return `${year}-${month}-${day}T${hours}:${minutes}`;
                }

                function renderNewsSlides() {
                  const container = document.getElementById("newsSlides");
                  const totalSlides = Math.ceil(
                    newsData.length / itemsPerSlide,
                  );

                  container.innerHTML = "";

                  for (let i = 0; i < totalSlides; i++) {
                    const slide = document.createElement("div");
                    slide.className = "news-slide" + (i === 0 ? " active" : "");

                    const startIdx = i * itemsPerSlide;
                    const endIdx = Math.min(
                      startIdx + itemsPerSlide,
                      newsData.length,
                    );

                    for (let j = startIdx; j < endIdx; j++) {
                      const item = newsData[j];
                      const newsCard = document.createElement("div");
                      newsCard.className = "news-card";

                      const date = new Date(item.date);
                      const formattedDate = date.toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                      });

                      newsCard.innerHTML = `
        <span class="badge bg-info text-white">${formattedDate}</span>
        <h5>${item.title}</h5>
        <a href="${item.link}" target="_blank" class="btn btn-sm btn-outline-primary">Read →</a>
      `;

                      slide.appendChild(newsCard);
                    }

                    container.appendChild(slide);
                  }

                  document.getElementById("totalSlides").textContent =
                    totalSlides;
                }

                function updateSlideDisplay() {
                  const slides = document.querySelectorAll(".news-slide");
                  slides.forEach((slide, idx) => {
                    slide.classList.remove("active");
                  });
                  if (slides[currentSlideIndex]) {
                    slides[currentSlideIndex].classList.add("active");
                  }
                  document.getElementById("currentSlide").textContent =
                    currentSlideIndex + 1;
                }

                document.addEventListener("DOMContentLoaded", function () {
                  const prevBtn = document.getElementById("prevBtn");
                  const nextBtn = document.getElementById("nextBtn");

                  if (prevBtn) {
                    prevBtn.addEventListener("click", () => {
                      const totalSlides = Math.ceil(
                        newsData.length / itemsPerSlide,
                      );
                      currentSlideIndex =
                        (currentSlideIndex - 1 + totalSlides) % totalSlides;
                      updateSlideDisplay();
                    });
                  }

                  if (nextBtn) {
                    nextBtn.addEventListener("click", () => {
                      const totalSlides = Math.ceil(
                        newsData.length / itemsPerSlide,
                      );
                      currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
                      updateSlideDisplay();
                    });
                  }
                });
              