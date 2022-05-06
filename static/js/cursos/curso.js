function uuidv4() {
	return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
		(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
	);
}

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
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

	this.createPost = function () {

		const post = {
			"id": uuidv4(),
			"title": this.postTitle(),
			"description": this.postDescription(),
			"dateCreated": new Date().toUTCString(),
			"answers": []
		}

		this.posts.push(post);
		
		const {guid} = getUrlVars();
		let cursos =JSON.parse(localStorage.getItem('cursos'));

		cursos.forEach(curso => {
			if(curso.id == guid) {
				curso.posts = this.posts();
			}
		});

		localStorage.setItem('cursos', JSON.stringify(cursos));
		
		$('#exampleModalCenter').modal('toggle');
		this.postTitle("");
		this.postDescription("");
		location.reload();
	}

	this.loadHomework = function({id}) {
		console.log(id);
		window.location.href = '/tareaAlumno?guid=' + id;
	}

	$(document).ready(() => {
		const {guid} = getUrlVars();
		let cursos = JSON.parse(localStorage.getItem('cursos'));

		cursos = cursos.filter(curso => curso.id == guid)[0];		

		console.log(cursos)

		this.title(cursos.name);
		this.description(cursos.description);
		this.posts(cursos.posts);
		this.professor(cursos.professor.name);
	});
}

ko.applyBindings(new CursoViewModel());