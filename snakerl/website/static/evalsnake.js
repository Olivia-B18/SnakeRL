/* sidebar content to show/hide */
const hideEvalSidebarDiv = document.getElementById("hideEvalSidebar")
const hideOneEpisodeScoreDiv = document.getElementById("hideOneEpisodeScore")
const hideHighestScoreDiv = document.getElementById("hideHighestScore")
const hideAvgScoreDiv = document.getElementById("hideAvgScore")

/* other variables */
let running = false;

/* hide sidebar content upon first page load */
hideEvalSidebarDiv.style.display = "none";
hideOneEpisodeScoreDiv.style.display = "none";
hideHighestScoreDiv.style.display = "none";
hideAvgScoreDiv.style.display = "none";

/* what to do when evalOnceBtn is clicked */
document.getElementById("evalOnceBtn").addEventListener("click", function () {
    if (!running) {
        // running = true;
        // const trainingInputValues = Object.fromEntries(
        //     Array.from(trainingInputElements, (slider) => [slider.id, slider.value])
        // );
        // socket.emit("train", trainingInputValues);

        /* show/hide sidebar content */
        hideEvalSidebarDiv.style.display = "block";
        hideOneEpisodeScoreDiv.style.display = "block";
        hideHighestScoreDiv.style.display = "none";
        hideAvgScoreDiv.style.display = "none";
    }
})

/* what to do when evalTenBtn is clicked */
document.getElementById("evalTenBtn").addEventListener("click", function () {
    if (!running) {
        // running = true;
        // const trainingInputValues = Object.fromEntries(
        //     Array.from(trainingInputElements, (slider) => [slider.id, slider.value])
        // );
        // socket.emit("train", trainingInputValues);

        /* show/hide sidebar content */
        hideEvalSidebarDiv.style.display = "block";
        hideOneEpisodeScoreDiv.style.display = "none";
        hideHighestScoreDiv.style.display = "block";
        hideAvgScoreDiv.style.display = "block";
    }
})