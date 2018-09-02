console.log('running tester')

function make_notification() {
    var r = new XMLHttpRequest();
    r.open("GET", '/test_make/', true);
    r.send();
}

function mark_all_as_read() {
    var r = new XMLHttpRequest();
    r.open("GET", '/mark_all_as_read/', true);
    r.send();
}