function uuidv4() {
	return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
		(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
	);
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

function getUrlVars() {
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for (var i = 0; i < hashes.length; i++) {
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	return vars;
}


function CursoViewModel() {

	this.title = ko.observable("");
	this.description = ko.observable("");
	this.posts = ko.observableArray([]);
	this.professor = ko.observable("");
	this.postTitle = ko.observable("");
	this.postDescription = ko.observable("");
	this.owner = ko.observable(false);
	this.enrolled = ko.observable(false);

	this.showEnrollButton = function () {
		return !this.enrolled() && !this.owner()
	}

	this.createPost = function () {
		const { guid } = getUrlVars();

		const payload = {
			"course": guid,
			"title": this.postTitle(),
			"content": this.postDescription()
		}

		axios.post('api/cursos/post/new/', payload, {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		})
		.then(response => {
			this.postTitle("");
			this.postDescription("");
			location.reload();
		}).catch(error => {
			console.error(error);
		});
	}

	this.loadHomework = function ({ id }) {
		console.log(id);
		window.location.href = '/tareaAlumno?guid=' + id;
	}

	$(document).ready(() => {
		const { guid } = getUrlVars();

		axios.get(`api/cursos/get/${guid}`, {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		}).then(response => {
			console.log(response)
			this.title(response.data.title);
			this.description(response.data.description);
			this.professor(response.data.professor.name);
			this.posts(response.data.posts);
			this.enrolled(response.data.enrolled);
			this.owner(response.data.owner);
		}).catch(error => {
			console.error(error);
		})
	});
}

ko.applyBindings(new CursoViewModel());