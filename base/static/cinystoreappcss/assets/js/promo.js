const navbar = document.getElementById('promoNavbar');
const logoNames = document.getElementById("logoName");
const logoSub = document.getElementById("logoSub");
window.onscroll = () => {
    if (window.scrollY > 60) {
        navbar.style.backgroundColor = "#fff";
        logoNames.style.color = "#000";
        logoSub.style.color = "#000";
    } else {
        navbar.style.backgroundColor = "transparent";
        logoNames.style.color = "#fff";
        logoSub.style.color = "#fff";
    }
};




const promoFooterSubBtnEl = document.getElementById("promoFooterSubBtn");
const promoFooterEl = document.getElementById("promoFooter");
const promoLabelMainContainerEl = document.getElementById("promoLabelMainContainer")

function myFunction(){
    promoFooterEl.style.display = "none";
}


promoFooterSubBtnEl.addEventListener("click", myFunction)