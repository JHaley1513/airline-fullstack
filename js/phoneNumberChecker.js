console.log('Phone number checker loaded');
//phoneNumberChecker allows only numbers to be input in the phone number fields.

//took the below code from https://stackoverflow.com/questions/469357/html-text-input-allow-only-numeric-input

// Restricts input for the given textbox to the given inputFilter.
function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      }
    });
  });
}

setInputFilter(document.getElementById("phone1"), function(value) {
  return /^\d*$/.test(value); //makes sure the input is a positive integer. Works even when copy-pasting into the input field.
});

setInputFilter(document.getElementById("phone2"), function(value) {
  return /^\d*$/.test(value);
});

setInputFilter(document.getElementById("phone3"), function(value) {
  return /^\d*$/.test(value);
});
