window.addEventListener("load", () => {
  for (let list of document.querySelectorAll(".concept-list ul li ul")) {
    let tog = document.createElement("div");
    tog.innerHTML = list.previousSibling.textContent;
    tog.className = "toggle";
    tog.onclick = () => tog.classList.toggle("show");
    list.parentElement.removeChild(list.previousSibling);
    list.parentElement.insertBefore(tog, list);
  }

  for (let list of document.querySelectorAll(".list-hierarchy")) {
    let btn_expand = document.createElement("button");
    btn_expand.innerHTML = "expand all";
    btn_expand.className = "btn-expand";
    btn_expand.onclick = () => {
      for (let div of list.getElementsByTagName("div")) {
        if (div.classList.contains("show")) { }
        else { div.classList.add("show"); }
      }
    };

    let btn_collapse = document.createElement("button");
    btn_collapse.innerHTML = "collapse all";
    btn_collapse.className = "btn-collapse";
    btn_collapse.onclick = () => {
      for (let div of list.getElementsByTagName("div")) {
        if (div.classList.contains("show")) { div.classList.remove("show"); }
        else { }
      }
    };
    list.insertBefore(btn_collapse, list.firstChild);
    list.insertBefore(btn_expand, btn_collapse);
  }
});