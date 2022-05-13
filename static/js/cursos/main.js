function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
  }

function CursosViewModel() {
	this.cursos = ko.observableArray([]);
	this.loading = ko.observable(true);
	this.canCreate = ko.observable(false);
	this.empty = ko.observable(true);

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
		
		const payload = {
			'name': this.cursoName(),
			'description': this.cursoDescription()
		}

		axios.post('api/cursos/new/', payload, {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		}).then(response => {
			$('#exampleModalCenter').modal('toggle');
			this.cursoName("");
			this.cursoDescription("");
			localStorage.setItem("cursos", JSON.stringify(this.cursos()));
			location.reload();
		}).catch(error => {
			console.error(error);
		});
	}

	$(document).ready(() => {
		axios.get('api/cursos/get/all', {
			headers: {
				'Authorization': 'Bearer ' + getCookie('token')
			}
		})
		.then(response => {
			console.log("test")
			this.loading(false);
			this.cursos(response.data.courses);
			this.canCreate(getCookie("type") == 1 ? true : false);
			this.empty(response.data.courses.length == 0 ? true : false);
		})
		.catch(error => {
			this.loading(true);
			console.error(error);
			this.canCreate(false);
		});
	})

}

ko.applyBindings(new CursosViewModel());