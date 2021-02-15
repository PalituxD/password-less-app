#! /bin/bash
function my-app-python-activate() {
  source $(poetry env info --path)/bin/activate
}

function my-app-python-deactivate() {
  deactivate
}
