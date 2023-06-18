function filter(n, l, key = null) {
  list = document.getElementById(l).children;
  if (key != null) {
    for (const i of list) {
      i.classList.add("hidden");
      for (let k = 0; k < i.classList.length; k++) {
        if (
          i.classList[k].toLowerCase().includes(n) &&
          i.classList[k].toLowerCase().includes(key)
        ) {
          i.classList.remove("hidden");
          break;
        }
      }
    }
  } else {
    for (const i of list) {
      if (i.innerText.toLowerCase().includes(n)) {
        i.classList.remove("hidden");
      } else {
        i.classList.add("hidden");
      }
    }
  }
}