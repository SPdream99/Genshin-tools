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
              star_character(char_list, "list");
            }
          });
      } else if (check.status_code == 400) {
        location.reload();
      }
    });
}

async function read_mat() {
  list = {};
  for (let i = 0; i < uplist.meta.length; i++) {
    const e = uplist.meta[i];
    list[e] = 0;
  }
  as_list = uplist.list.asc;
  ts_list = uplist.list.tl;
  lv = parseInt(document.getElementById("lv_box").value);
  if (lv <= 90 && lv > 1) {
    list.exp = getEXP(lv - 2);
    a = ((list.exp % 20000) % 5000) % 1000;
    if (a == 0) {
      list["mora"] += list.exp / 5;
    } else {
      list["mora"] += (list.exp - a + 1000) / 5;
    }
  }
  as_lv = parseInt(document.getElementById("as_box").value);
  if (as_lv <= 7 && as_lv > 1) {
    for (const i of Object.keys(as_list)) {
      if (parseInt(i) + 1 <= as_lv) {
        let l = as_list[i];
        for (const r of Object.keys(l)) {
          list[r] += parseInt(l[r].replaceAll(",", ""));
        }
      } else {
        break;
      }
    }
  }
  for (let i = 0; i < 3; i++) {
    ts_lv = parseInt(document.getElementById(`ts${i + 1}_box`).value);
    if (ts_lv <= 10 && ts_lv > 1) {
      for (const i of Object.keys(ts_list)) {
        if (parseInt(i) <= ts_lv) {
          let l = ts_list[i];
          for (const r of Object.keys(l)) {
            list[r] += parseInt(l[r].replaceAll(",", ""));
          }
        } else {
          break;
        }
      }
    }
  }
  const responsed = await fetch(`/material/change`, {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  check = await responsed.json();
  mats_list = {};
  if (check.status_code == 200) {
    if (check.content.items == null) {
      mats_list = {};
    } else {
      mats_list = check.content.items;
      mats_list = JSON.parse(mats_list);
    }
  }
  for (let i = 0; i < uplist.meta.length; i++) {
    n = uplist.meta[i];
    q = list[n];
    if (q <= 0) {
      hide(n);
    } else {
      change(q, n, `${n}_modal`, mats_list);
    }
  }

  function getEXP(n) {
    exp = [
      1000, 1325, 1700, 2150, 2625, 3150, 3725, 4350, 5000, 5700, 6450, 7225,
      8050, 8925, 9825, 10750, 11725, 12725, 13775, 14875, 16800, 18000, 19250,
      20550, 21875, 23250, 24650, 26100, 27575, 29100, 30650, 32250, 33875,
      35550, 37250, 38975, 40750, 42575, 44425, 46300, 50625, 52700, 54775,
      56900, 59075, 61275, 63525, 65800, 68125, 70475, 76500, 79050, 81650,
      84275, 86950, 89650, 92400, 95175, 98000, 100875, 108950, 112050, 115175,
      118325, 121525, 124775, 128075, 131400, 134775, 138175, 148700, 152375,
      156075, 159825, 163600, 167425, 171300, 175225, 179175, 183175, 216225,
      243025, 273100, 306800, 344600, 386950, 434425, 487625, 547200,
    ];
    cost = 0;
    for (let i = 0; i <= n; i++) {
      const e = exp[i];
      cost += e;
    }
    return cost;
  }

  function change(n, id, modal, lss) {
    if (lss != {}) {
      own = lss[id] || 0;
      id = document.getElementById(id);
      modal = document.getElementById(modal);
      id.classList.remove("hidden");
      id.getElementsByTagName("p")[1].innerText = n.toLocaleString();
      modal.getElementsByClassName("quantity")[0].children[1].innerText =
        n.toLocaleString();
      modal.getElementsByClassName(
        "quantity"
      )[0].children[2].innerText = `(have: ${own.toLocaleString()})`;
      if (n < own) {
        modal.getElementsByClassName(
          "quantity"
        )[0].children[3].innerText = `(need: ${(0).toLocaleString()})`;
      } else {
        modal.getElementsByClassName(
          "quantity"
        )[0].children[3].innerText = `(need: ${(n - own).toLocaleString()})`;
      }
    } else {
      id.getElementsByTagName("p")[1].innerText = n.toLocaleString();
      modal.getElementsByClassName("quantity")[0].children[1].innerText =
        n.toLocaleString();
      modal.getElementsByClassName(
        "quantity"
      )[0].children[2].innerText = `(have: ${(0).toLocaleString()})`;
      modal.getElementsByClassName(
        "quantity"
      )[0].children[3].innerText = `(need: ${n.toLocaleString()})`;
    }
  }

  function hide(id) {
    id = document.getElementById(id);
    if (!id.classList.contains("hidden")) {
      id.classList.add("hidden");
    }
  }
}

function render_mat(l) {
  l = JSON.parse(l);
  t = document.getElementById("side_list").children;
  if (t.length < Object.keys(l).length) {
    location.reload();
  }
  for (let i = 0; i < t.length; i++) {
    ele = t[i].id.replace("side_", "");
    if (ele in l) {
      o = document
        .getElementById("side_" + ele + "_modal")
        .getElementsByClassName("quantity");
      t[i].getElementsByTagName("p")[1].innerText = l[ele].toLocaleString();
      o[0].children[1].innerText = l[ele].toLocaleString();
      if (t[i].classList.contains("hidden")) {
        t[i].classList.remove("hidden");
      }
    } else {
      if (!t[i].classList.contains("hidden")) {
        t[i].classList.add("hidden");
      }
    }
  }
  read_mat();
}

function set_mat(mat, quantity) {
  quantity = document.getElementById(quantity).value;
  quantity = parseInt(quantity);
  if (!isNaN(quantity)) {
    fetch(`/material/change`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: mat,
        quantity: quantity,
      }),
    })
      .then((response) => response.json())
      .then((response) => {
        check = response;
        if (check.status_code == 200) {
          fetch(`/material/change`, {
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
                if (check.content.items == null) {
                  mats_list = {};
                } else {
                  mats_list = check.content.items;
                }
                render_mat(mats_list);
              }
            });
        } else if (check.status_code == 400) {
          location.reload();
        }
      });
  }
}
