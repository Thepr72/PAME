function uuidv4() {
	return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
		(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
	);
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


function TareaAlumnoViewModel() {

	this.title = ko.observable("default");
	this.description = ko.observable("default");
	this.postDescription = ko.observable("");
	this.freezeAnswer = ko.observable(false);

	this.createPost = function () {
		const gg = getUrlVars();
		const post = {
			"id": uuidv4(),
			"postId": gg.id,
			"description": this.postDescription(),
			"dateCreated": new Date().toUTCString(),
		}


		const { guid } = getUrlVars();
		let cursos = JSON.parse(localStorage.getItem('cursos'));

		cursos.forEach(curso => {
			for (let i = 0; i < curso.posts.length; i++) {
				if (curso.posts[i].id == guid) {
					curso.posts[i].answers.push(post);
				}
			}
		});

		localStorage.setItem('cursos', JSON.stringify(cursos));

		$('#exampleModalCenter').modal('toggle');
		this.postDescription("");
		location.reload();
	}


	$(document).ready(() => {
		const { guid } = getUrlVars();
		let cursos = JSON.parse(localStorage.getItem('cursos'));

		cursos = cursos.filter(curso => {
			for (let i = 0; i < curso.posts.length; i++) {
				if (curso.posts[i].id == guid) {
					return true
				}
			}

			return false
		})[0];

		cursos = cursos.posts.filter(post => post.id == guid)[0];

		console.log(cursos)

		if(cursos.answers.length > 0) {
			this.freezeAnswer(true);
			this.postDescription(cursos.answers[0].description);
		}


		this.title(cursos.title);
		this.description(cursos.description);
	});
}

ko.applyBindings(new TareaAlumnoViewModel());