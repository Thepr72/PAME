function uuidv4() {
	return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
		(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
	);
}

function CursosViewModel() {
	this.cursos = ko.observableArray([]);

	this.cursos.subscribe((val) => {
		console.log(val)
	});

	this.cursoName = ko.observable("");
	this.cursoDescription = ko.observable("");

	this.cursoName.subscribe((val) => {
		console.log(val);
	});

	this.cursoDescription.subscribe((val) => {
		console.log(val);
	});

	this.openCourse = function ({ id }) {
		console.log(id);
		window.location.href = '/curso?guid=' + id;
	}

	this.openCourseAlumno = function({id}) {
		console.log(id);
		window.location.href = '/cursoAlumno?guid=' + id;
	}

	this.addCurso = function () {
		this.cursos.push({
			"id": uuidv4(),
			"name": this.cursoName(),
			"description": this.cursoDescription(),
			"professor": {
				"name": "Profesor Demo"
			},
			"posts": [],
			"password": false
		});

		$('#exampleModalCenter').modal('toggle');
		this.cursoName("");
		this.cursoDescription("");
		localStorage.setItem("cursos", JSON.stringify(this.cursos()));
		location.reload();
	}

	$(document).ready(() => {
		console.log('here')
		const tempCursos = JSON.parse(localStorage.getItem('cursos'));
		this.cursos(tempCursos == null ? [] : tempCursos);
	})
}

ko.applyBindings(new CursosViewModel());