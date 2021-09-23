let creatingState = "";

$(".create-file").click(function () {
    creatingState = "file";
});

$(".create-folder").click(function () {
    creatingState = "folder";
});

$(".create-confirm").click(function () {
    socket.emit("create", {type: creatingState, name: $("#ffName").val()});
});
