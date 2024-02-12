const ADDON_PREFIX = "study_review_deck_buttons_addon";

function main() {
  on_added(".new-count", async (element) => {
    let learned_today = await cmd("get_learned_today_count");
    element.textContent += `(${learned_today})`;
  });
}

window.addEventListener("DOMContentLoaded", main);

//
// Utility functions.

function on_added(selector, callback) {
  let processed_nodes = new Set();
  let observer = new MutationObserver((mutationsList, observer) => {
    for (let mutation of mutationsList) {
      if (mutation.type === "childList") {
        let element = document.querySelector(selector);
        if (element && !processed_nodes.has(element)) {
          observer.disconnect();
          processed_nodes.add(element);
          callback(element);
          observer.observe(document, { childList: true, subtree: true });
        }
        mutation.removedNodes.forEach((node) => {
          if (node.matches && node.matches(selector)) {
            processed_nodes.delete(node);
          }
        });
      }
    }
  });
  observer.observe(document, { childList: true, subtree: true });
}

// Prefix string with a unique addon identifier to avoid name collisions.
function pre(string) {
  return `${ADDON_PREFIX}_${string}`;
}

// Send a command to the Anki addon. You can await for the return value.
async function cmd(command, ...arg) {
  return new Promise((resolve, _reject) => {
    pycmd(pre(command) + ":" + arg.join(":"), (ret) => {
      resolve(ret);
    });
  });
}