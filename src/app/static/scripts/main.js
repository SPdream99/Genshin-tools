function filter_text(n, l) {
  n = n.toLowerCase();
  list = document.getElementById(l).children;
  for (const i of list) {
    if (i.innerText.toLowerCase().includes(n)) {
      i.classList.remove("hidden");
    } else {
      i.classList.add("hidden");
    }
  }
}

function filter(t, ol, l, key) {
  if (!t.classList.contains("f-enable")) {
    t.classList.add("f-enable");
  } else {
    t.classList.remove("f-enable");
  }
  tl = [];
  for (const i of ol) {
    o = [];
    a = document.getElementById(i).children;
    for (const j of a) {
      if (j.classList.contains("f-enable")) {
        for (const k of j.classList) {
          if (check_include(k, key)) {
            o.push(k.toLowerCase());
            break;
          }
        }
      }
    }
    if (o.length > 0) {
      tl.push(o);
    }
  }
  list = document.getElementById(l).children;
  for (const i of list) {
    i.classList.remove("s-hidden");
    for (n = 0; n < tl.length; n++) {
      if (!check_include(tl[n], i.classList)) {
        if (!i.classList.contains("s-hidden")) {
          i.classList.add("s-hidden");
        }
      }
    }
  }
  if (tl.length == 0) {
    for (const i of list) {
      i.classList.remove("s-hidden");
    }
  }
}

function check_include(v, l) {
  for (const i of l) {
    if (v.includes(i)) {
      return true;
    }
  }
  return false;
}

function star_character(cl, l) {
  list = document.getElementById(l).children;
  for (const i of list) {
    i.classList.remove("star-n");
    i.classList.remove("star-y");
    if (cl.includes(i.id.toLowerCase())) {
      if (!i.classList.contains("star-y")) {
        i.classList.add("star-y");
      }
    } else {
      if (!i.classList.contains("star-n")) {
        i.classList.add("star-n");
      }
    }
  }
}

function star(char) {
  fetch(`/characters/star/check`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: char,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      check = response;
      if (check.status_code == 200) {
        fetch(`/characters/star/list`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((response) => {
            check = response;
            if (check.status_code == 200) {
              if (check.content.char == null) {
                char_list = [];
              } else {
                char_list = check.content.char;
              }
              console.log(char_list);
              star_character(char_list, "list");
            }
          });
      } else if (check.status_code == 400) {
        location.reload();
      }
    });
}
