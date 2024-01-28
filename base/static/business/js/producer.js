
const dashboardEl = document.getElementById("dashboard");
const contentEl = document.getElementById("content");
const accountEl = document.getElementById("account");

const dashboardTextEl = document.getElementById("dashboardText");
const contentTextEl = document.getElementById("contentText");
const accountTextEl = document.getElementById("accountText");

function functionDashboard(){
    dashboardEl.classList.add("options-bg-color-active");
    contentEl.classList.remove("options-bg-color-active");
    accountEl.classList.remove("options-bg-color-active");

    dashboardTextEl.classList.add("options-text-color-active");
    contentTextEl.classList.remove("options-text-color-active");
    accountTextEl.classList.remove("options-text-color-active");
}

function functionContent(){
    dashboardEl.classList.remove("options-bg-color-active");
    contentEl.classList.add("options-bg-color-active");
    accountEl.classList.remove("options-bg-color-active");

    dashboardTextEl.classList.remove("options-text-color-active");
    contentTextEl.classList.add("options-text-color-active");
    accountTextEl.classList.remove("options-text-color-active");
}

function functionAccount(){
    dashboardEl.classList.remove("options-bg-color-active");
    contentEl.classList.remove("options-bg-color-active");
    accountEl.classList.add("options-bg-color-active");

    dashboardTextEl.classList.remove("options-text-color-active");
    contentTextEl.classList.remove("options-text-color-active");
    accountTextEl.classList.add("options-text-color-active");
}

dashboardEl.addEventListener("click", functionDashboard);
contentEl.addEventListener("click", functionContent);
accountEl.addEventListener("click", functionAccount);


/*.........................................................*/
const labelsBtnEl = document.getElementById("labelsBtn");
const postsBtnEl = document.getElementById("postsBtn");
const clipsBtnEl = document.getElementById("clipsBtn");

const labelsEl = document.getElementById("labels");
const postsEl = document.getElementById("posts");
const clipsEl = document.getElementById("clips");

labelsEl.style.display = "block";
postsEl.style.display = "none";
clipsEl.style.display = "none";

labelsBtnEl.classList.add("producer-content-headings-btn-active");
postsBtnEl.classList.remove("producer-content-headings-btn-active");
clipsBtnEl.classList.remove("producer-content-headings-btn-active");


function functionLabels(){
    labelsEl.style.display = "block";
    postsEl.style.display = "none";
    clipsEl.style.display = "none";

    labelsBtnEl.classList.add("producer-content-headings-btn-active");
    postsBtnEl.classList.remove("producer-content-headings-btn-active");
    clipsBtnEl.classList.remove("producer-content-headings-btn-active");
}

function functionPosts(){
    labelsEl.style.display = "none";
    postsEl.style.display = "block";
    clipsEl.style.display = "none";

    labelsBtnEl.classList.remove("producer-content-headings-btn-active");
    postsBtnEl.classList.add("producer-content-headings-btn-active");
    clipsBtnEl.classList.remove("producer-content-headings-btn-active");
}

function functionClips(){
    labelsEl.style.display = "none";
    postsEl.style.display = "none";
    clipsEl.style.display = "block";

    labelsBtnEl.classList.remove("producer-content-headings-btn-active");
    postsBtnEl.classList.remove("producer-content-headings-btn-active");
    clipsBtnEl.classList.add("producer-content-headings-btn-active");
}

labelsBtnEl.addEventListener("click", functionLabels);
postsBtnEl.addEventListener("click", functionPosts);
clipsBtnEl.addEventListener("click", functionClips);


