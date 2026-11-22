const replay = document.getElementById("replay");
const toggle = document.getElementById("play");
const clip = document.getElementById("clip");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const allowAutoPlay = () =>
  !reducedMotion.matches && !navigator.connection?.saveData;
const records = {
  "placement-feedback": [
    "pick-place",
    "event5",
    202611204,
    10,
    "A missed command",
    "Five translations are suppressed as Fetch approaches the cube. Re-encoding from the measured hand with feedback completes this layout.",
  ],
  "placement-copy": [
    "pick-place",
    "copy",
    202611204,
    10,
    "The same missed command",
    "The same layout and five overwritten translations, with the recorded command copied directly. The cube misses the final placement goal.",
  ],
  "push-feedback": [
    "push",
    "event5",
    202611203,
    8,
    "Pushing with hand feedback",
    "After five overwritten translations, the measured hand supplies the reference for re-encoding. The push reaches the final goal on this layout.",
  ],
  "push-copy": [
    "push",
    "copy",
    202611203,
    8,
    "A push falls short",
    "With direct copying, the five overwritten translations disrupt the push. The cube finishes outside the success region.",
  ],
};
function reflectPlayback() {
  const playing = !replay.paused && !replay.ended;
  document.getElementById("play-label").textContent = playing
    ? "Pause"
    : "Play";
  document.getElementById("play-icon").textContent = playing ? "Ⅱ" : "▷";
  toggle.setAttribute("aria-label", playing ? "Pause replay" : "Play replay");
}
function playReplay() {
  if (!replay.getAttribute("src")) replay.src = replay.dataset.file;
  replay.muted = true;
  replay.play().catch(reflectPlayback);
}
for (const event of ["play", "pause", "ended"])
  replay.addEventListener(event, reflectPlayback);
toggle.addEventListener("click", () =>
  replay.paused ? playReplay() : replay.pause(),
);
reducedMotion.addEventListener("change", () => {
  if (reducedMotion.matches) replay.pause();
});
clip.addEventListener("change", () => {
  const [task, method, seed, onset, title, description] = records[clip.value];
  const wasPlaying = !replay.paused;
  replay.pause();
  replay.removeAttribute("src");
  replay.load();
  replay.dataset.file = `assets/videos/ral-fetch-${task}-drop-${method}-${seed}-1080p.mp4`;
  replay.poster = `assets/videos/ral-${task}-${method}-poster.jpg`;
  replay.setAttribute(
    "aria-label",
    `${task} simulated replay, ${method === "copy" ? "direct copy" : "measured hand feedback"}`,
  );
  document.getElementById("replay-title").textContent = title;
  document.getElementById("replay-copy").textContent = description;
  document.getElementById("task").textContent =
    task === "push" ? "Push" : "Pick and place";
  document.getElementById("seed").textContent = seed;
  document.getElementById("onset").textContent = `Step ${onset}`;
  if (wasPlaying) playReplay();
  else reflectPlayback();
});
if (allowAutoPlay()) playReplay();

document.querySelectorAll('input[name="stage"]').forEach((input) =>
  input.addEventListener("change", () => {
    document.getElementById("guard-note").textContent =
      input.value === "delivered"
        ? "All 560 reached the setter and reduced squared error on that write."
        : "These 98 passed the guard but the receiver suppressed the translation. No rewrite reached the setter.";
  }),
);
function showCount(element, value, unit) {
  const small = document.createElement("small");
  small.textContent = unit;
  element.replaceChildren(document.createTextNode(value + " "), small);
}
document.getElementById("cycle").addEventListener("change", (event) => {
  showCount(
    document.getElementById("error-range"),
    event.target.value === "1" ? "0.074–0.144" : "0.585–0.791",
    "mm",
  );
});
document.getElementById("cohort").addEventListener("change", (event) => {
  const second = event.target.value === "second";
  showCount(
    document.getElementById("droid-count"),
    second ? "176" : "81",
    second ? "of 4,551 rows" : "of 2,610 rows",
  );
  document.getElementById("droid-note").textContent = second
    ? "Retained rows with different flags at observation and action time. One recording accounted for 105 of the 176 differences."
    : "Retained rows with different flag values across the two sampling times.";
});
document.getElementById("copy-cite").addEventListener("click", async () => {
  const citation = document.getElementById("citation");
  const status = document.getElementById("copy-state");
  try {
    await navigator.clipboard.writeText(citation.textContent);
    status.textContent = " Citation copied.";
  } catch {
    const range = document.createRange();
    range.selectNodeContents(citation);
    const selection = getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = " Citation selected. Use your device’s copy command.";
  }
});
const callbackSchedule = document.getElementById("cycle");
callbackSchedule.addEventListener("change", () => {
  const slow = callbackSchedule.value === "10";
  const band = document.getElementById("rms-band");
  band.style.left = slow ? "58.5%" : "7.4%";
  band.style.width = slow ? "20.6%" : "7%";
});
const recordingCohort = document.getElementById("cohort");
recordingCohort.addEventListener("change", () => {
  const share =
    recordingCohort.value === "second" ? (100 * 176) / 4551 : (100 * 81) / 2610;
  document.getElementById("droid-band").style.width = `${share}%`;
  document.getElementById("droid-percent").textContent =
    `${share.toFixed(2)}% of retained rows`;
});
