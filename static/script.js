// Load statistics on page load
document.addEventListener("DOMContentLoaded", function () {
  loadStatistics();
});

// Handle form submission
document
  .getElementById("recommendationForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // Get form values
    const mood = document.getElementById("mood").value;
    const energy = document.getElementById("energy").value;

    // Validate
    if (!mood) {
      alert("Mohon pilih mood Anda!");
      return;
    }

    if (!energy) {
      alert("Mohon pilih level energi Anda!");
      return;
    }

    // Show loading
    document.getElementById("loading").style.display = "block";
    document.getElementById("results").style.display = "none";

    // Scroll to loading
    document.getElementById("loading").scrollIntoView({ behavior: "smooth" });

    try {
      // Send request to backend
      const response = await fetch("/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          mood: mood,
          energy: energy,
        }),
      });

      const data = await response.json();

      // Hide loading
      document.getElementById("loading").style.display = "none";

      if (response.ok) {
        displayRecommendations(data);
      } else {
        alert("Error: " + (data.error || "Something went wrong"));
      }
    } catch (error) {
      document.getElementById("loading").style.display = "none";
      alert("Error: " + error.message);
      console.error("Error:", error);
    }
  });

// Display recommendations
function displayRecommendations(data) {
  const resultsDiv = document.getElementById("results");
  const messageDiv = document.getElementById("resultMessage");
  const listDiv = document.getElementById("recommendationsList");

  // Show results
  resultsDiv.style.display = "block";
  messageDiv.textContent = data.message;

  // Clear previous results
  listDiv.innerHTML = "";

  // Check if recommendations exist
  if (!data.recommendations || data.recommendations.length === 0) {
    listDiv.innerHTML =
      '<p style="text-align: center; padding: 20px;">Tidak ada lagu yang ditemukan. Coba kriteria lain.</p>';
    resultsDiv.scrollIntoView({ behavior: "smooth" });
    return;
  }

  // Display each recommendation
  data.recommendations.forEach((song, index) => {
    const songCard = document.createElement("div");
    songCard.className = "song-card";
    songCard.innerHTML = `
            <div class="song-number">${index + 1}</div>
            <div class="song-title">🎵 ${song.song_name}</div>
            <div class="song-artist">🎤 ${song.artist}</div>
            <div class="song-details">
                <span class="detail-badge">🎸 ${song.genre}</span>
                <span class="detail-badge">😊 ${song.mood}</span>
                <span class="detail-badge">⚡ ${song.energy}</span>
                <span class="detail-badge">💃 ${song.danceability}</span>
                <span class="detail-badge">🎼 ${song.tempo} BPM</span>
            </div>
        `;
    listDiv.appendChild(songCard);
  });

  // Scroll to results
  resultsDiv.scrollIntoView({ behavior: "smooth" });
}

// Load statistics
async function loadStatistics() {
  try {
    const response = await fetch("/stats");
    const data = await response.json();

    if (response.ok) {
      displayStatistics(data);
    }
  } catch (error) {
    console.error("Error loading statistics:", error);
    document.getElementById("stats").innerHTML =
      "<p>Failed to load statistics.</p>";
  }
}

// Display statistics
function displayStatistics(data) {
  const statsDiv = document.getElementById("stats");

  let html = `
        <div class="stat-item">
            <h3>📀 Total Lagu</h3>
            <div class="stat-value">${data.total_songs}</div>
        </div>
        
        <div class="stat-item">
            <h3>🎸 Genre</h3>
            <ul class="stat-list">
                ${Object.entries(data.genres)
                  .map(([genre, count]) => `<li>${genre}: ${count}</li>`)
                  .join("")}
            </ul>
        </div>
        
        <div class="stat-item">
            <h3>😊 Mood</h3>
            <ul class="stat-list">
                ${Object.entries(data.moods)
                  .map(([mood, count]) => `<li>${mood}: ${count}</li>`)
                  .join("")}
            </ul>
        </div>
        
        <div class="stat-item">
            <h3>⚡ Energy Level</h3>
            <ul class="stat-list">
                ${Object.entries(data.energy_levels)
                  .map(([energy, count]) => `<li>${energy}: ${count}</li>`)
                  .join("")}
            </ul>
        </div>
    `;

  statsDiv.innerHTML = html;
}

// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
      });
    }
  });
});
