function fetchCloud() {
	let h1 = document.getElementById('title');
	searchContainer = document.getElementById('searchContainer');
	searchTerm = document.getElementById('searchTerm');
	searchLocation = document.getElementById('searchLocation');
	searchBar = document.getElementById('search');
	loadIcon = document.getElementById('loadIcon');

	searchContainer.style.opacity = '1';
	h1.style.top = '0px';
	h1.style.fontSize = '28px';
	searchBar.style.opacity = '0';
	loadIcon.style.zIndex = '10';
	loadIcon.style.opacity = '1';
	searchBar.style.cursor = 'none';
	console.log('test');


}

function hoverCloud() {
	searchContainer = document.getElementById('searchContainer');
	searchTerm = document.getElementById('searchTerm');
	searchLocation = document.getElementById('searchLocation');
	searchBar = document.getElementById('search');

	searchTerm.style.backgroundColor = 'white';
	searchLocation.style.backgroundColor = 'white';
	searchBar.style.opacity = '1';
}


function resultsContainer() {
	resultsContainer = document.getElementById('results_container');
	resultsContainer.style.marginTop = "180px";
	// resultsContainer.style.position = 'absolute';
	header()
}

function header(){
	let header = document.getElementById('headerLogo');
	header.style.top = '45px';
	header.style.opacity = '1';
}

function clearFields() {
	frm = document.getElementsByTagName('FORM');
	frm.reset();  // Reset all form data
	return false;

}

function abort() {
	resultsContainer = document.getElementById('results_container');
	resultsContainer.style.marginTop = '100vh';

	searchBar = document.getElementById('search');
	loadIcon = document.getElementById('loadIcon');
	searchBar.style.opacity = '1';
	loadIcon.style.zIndex = '-10';
	loadIcon.style.opacity = '0';

	let h1 = document.getElementById('title');
	h1.style.top = '0px';
	h1.style.fontSize = '60px';

	let header = document.getElementById('headerLogo');
	header.style.top = '45px';
	header.style.opacity = '0';

}

function cloudClick() {

	cloudWrap = document.getElementById('cloud_wrapper');

	if (cloudWrap.style.overflow === 'visible') {
		console.log('hidden');
		cloudWrap.style.overflow = 'hidden';
		cloudWrap.classList.remove('no-hover');
		cloudWrap.style.transition = 'all 0.5s';
		cloudWrap.classList.add('hover');
	} else {
		console.log('visible');
		cloudWrap.classList.remove('hover');
		cloudWrap.classList.add('no-hover');
		cloudWrap.style.transition = 'none';
		cloudWrap.style.overflow = 'visible';
	}

}

//POST SEARCH
$(function () {

	$('form').on('submit', function (e) {

		e.preventDefault();

		$.ajax({
			type: 'post',
			url: '/getIP',
			data: $('form').serialize(),
			success: function (data) {
				var output = JSON.stringify(data.wordcloud);
				var stripped = output.slice(1,-2);
				$('#cloud').attr('src', stripped);
				resultsContainer();
			}
		});

	});

});
