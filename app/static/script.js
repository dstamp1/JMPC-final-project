document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var options = {}
    var instances = M.FormSelect.init(elems, options);
  });
  
document.addEventListener('DOMContentLoaded', function() {
    var options = {
        onChipAdd() {
            console.log("added");
        },
        onChipSelect() {
            console.log("Selected");
        },
        onChipDelete() {
            console.log("Deleted");
        },
        placeholder: 'Tag your rule',
        secondaryPlaceholder: '+tag',
    }
    var elems = document.querySelector('.chips');
    var instances = M.Chips.init(elems, options);
});

function collectTags() {
    var chips_data = M.Chips.getInstance($('.chips')).chipsData;
    chips_data.forEach(data => {
        console.log(data.tag);
        $('form').append('<input type="hidden" name="tags" value="' + data.tag + '"/>')
    })
}
    