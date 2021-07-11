function change(a) {
  if (document.getElementById(a).value == '⌄'){
    document.getElementById(a).value = '⌃';
    document.getElementById("submit").submit();
    // document.getElementById(a).innerHTML = '⌃';
  } else {
    document.getElementById(a).value = '⌄';
    document.getElementById("submit").submit();
    // document.getElementById(a).innerHTML = '⌄';
  }
}
