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


function TareaAlumnoViewModel() {

	this.title = ko.observable("default");
	this.description = ko.observable("default");
	this.postDescription = ko.observable("");
	this.freezeAnswer = ko.observable(false);
	this.homeId = ko.observable(-1);

	this.createPost = function () {
		

		const payload = {
			"homework": this.homeId(),
			"answer": this.postDescription(),
		}

		axios.post('api/tareas/response/new/', payload, {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		})
		.then(response => {
			this.postDescription("");
			location.reload();
		})
		.error(error => {
			console.error(error);
		});


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

		axios.get('api/cursos/post/get/one/' + guid, {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		})
		.then(response => {
			console.log(response.data)
			this.title(response.data.title);
			this.description(response.data.description);
			this.freezeAnswer(response.data.response.id != null);
			this.postDescription(response.data.response.answer);
			this.homeId(response.data.id);
		})
		.catch(error => {
			console.error(error);
		});
	});
}

ko.applyBindings(new TareaAlumnoViewModel());