function genreDragStart(event) {
    event.dataTransfer.setData('text/genre_id', event.target.id);
}

function doDragOver(event) {
    if (event.dataTransfer.types[0] == 'text/genre_id') {
        event.preventDefault();
    }
}

function genreDrop(event, new_pool) {
    event.preventDefault();
    var data = event.dataTransfer.getData('text/genre_id');
    genre_id = Number(data.split('-')[1]);
    // move genre_id from old pool to new one
    console.log(event);
   moveGenre(genre_id, new_pool);
}

function moveGenre(genre_id, new_pool) {
    console.log(new_pool);
    // remove genre from old pool
    vm.genres_pool.remove(genre_id);
    vm.genres_include.remove(genre_id);
    vm.genres_exclude.remove(genre_id);
    // add to new pool
    switch (new_pool) {
        case 'genres_pool':
            vm.genres_pool.push(genre_id);
            break;
        case 'genres_include':
            vm.genres_include.push(genre_id);
            break;
        case 'genres_exclude':
            vm.genres_exclude.push(genre_id);
            break;
    }
    updateNumber();
}

function updateNumber() {
    $.ajax({
        url: '/movie/filter/',
        data: ko.toJS(vm),
        dataType: 'json',
        success: function(data) {
            var number;
            if (data.movies==100) {
                number = "100";
                $('#remaining > #text').html('+');
            }
            else {
                number = "00" + data.movies;
                number = number.substr(number.length-2);
                $('#remaining > #text').html('&nbsp;');
            }
            $('#movies_remaining').html(number);
        }
    })
}

function play_random() {
    $.ajax({
        url: '/movie/random/',
        data: ko.toJS(vm),
        dataType: 'json',
        success: function(data) {
            window.location.href = '/movie/'+data.choice;
        }
    })
}
