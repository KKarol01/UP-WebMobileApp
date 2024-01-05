// let URL = "http://192.168.1.31/api/"
// let URL = "http://localhost:8080/api"
let URL = "http://172.160.248.2/api"
axios.defaults.headers.common["Authorization"] = "Bearer " + window.localStorage.getItem("jwt")
axios.defaults.baseURL = URL + "/en"
let _URL = URL
URL = ""
if (window.localStorage.getItem("theme") == null) {
    window.localStorage.setItem("theme", "dark")
}
if (window.localStorage.getItem("lan") == null) {
    window.localStorage.setItem("lan", "EN")
}
document.querySelector("html").setAttribute("data-theme", window.localStorage.getItem("theme"))

document.addEventListener("alpine:init", () => {
    Alpine.store("logged_in", 0)
    Alpine.store("show", {
        show: 0,
        init() {
            if (window.localStorage.getItem("show")) {
                this.show = window.localStorage.getItem("show")
            }
        },
        set(val) {
            window.localStorage.setItem("show", val)
            this.show = val
        }
    })
    Alpine.store("show").init()
    if (window.localStorage.getItem("lan")) {
        Alpine.store("lan", window.localStorage.getItem("lan"))
    } else {
        Alpine.store("lan", "EN")
    }

    Alpine.data('register', () => ({
        email: '',
        password: '',
        password_repeat: '',
        error_message: '',
        try_register() {
            axios.post(URL + "register", { email: this.email, password: this.password, password_repeat: this.password_repeat })
                .then(e => {
                    if (e.status == 200) {
                        Alpine.store("show").set(1)
                    }
                }).catch(e => {
                    this.error_message = e.response.data.message
                })
        }
    }))

    Alpine.data('login', () => ({
        email: '',
        password: '',
        error_message: '',
        init() {
            axios.get(URL + "jwt").then(e => {
                if (e.status == 200) { Alpine.store("logged_in", 1) }
            }).catch(e => {
                if (e.status == 401) {
                    Alpine.store("logged_in", 0)
                }
            })
        },
        try_login() {
            axios.post(URL + "login", { email: this.email, password: this.password }, { withCredentials: true })
                .then(e => {
                    if (e.status == 200) {
                        console.log(this.email)
                        this.email = ''
                        this.password = ''
                        this.error_message = ''
                        Alpine.store("logged_in", 1)
                        window.localStorage.setItem("jwt", e.data.message.access_token)
                        axios.defaults.headers.common["Authorization"] = "Bearer " + window.localStorage.getItem("jwt")
                        Alpine.store("show").set(2)
                    }
                }).catch(e => {
                    this.error_message = e.response.data.message
                })
        },
        logout() {
            axios.get(URL + "logout", { withCredentials: true }).then(e => {
                Alpine.store("show").set(1)
            }).catch(e => {
            }).finally(() => {
                Alpine.store("logged_in", 0)
            })
        }
    }))

    Alpine.data("notes", () => ({
        notes: [],
        notes_settings: {},
        notes_updates: {},
        title: '',
        desc: '',
        tab: 0,
        error_message: '',
        page: 0,
        notesPerPage: 10,
        totalNotes: 0,
        totalPages: 0,
        deleteindex: -1,
        loading: 1,
        adding: 0,
        updating: 0,
        reset() {
            this.notes = []
            this.notes_settings = {}
            this.notes_updates = {}
            this.title = ''
            this.desc = ''
            this.tab = 0
            this.error_message = ''
            this.page = 0
            this.notesPerPage = 10
            this.totalNotes = 0
            this.totalPages = 0
            this.deleteindex = -1
        },
        isAuthorized() {
            return axios.get(URL + "jwt").then(e => {
                if (e.status == 200) { return true }
                return false
            }).catch(e => { return false })
        },
        getNotes() {
            this.loading = 1
            this.notes = []
            setTimeout(() => {
                axios.get(URL + `notes/${this.page * this.notesPerPage}/${this.notesPerPage}`, { withCredentials: true }).then(e => {
                    if (e.status == 200) {
                        this.loading = 0
                        this.notes = e.data.message.notes
                        this.notes_settings = {}
                    }
                }).catch(e => { this.loading = 0 })
                this.getNoteCount()
            }, 500)
        },
        getNoteCount() {
            axios.get(URL + `notecount`, { withCredentials: true }).then(e => {
                if (e.status == 200) {
                    this.totalNotes = e.data.message.count
                    this.totalPages = Math.floor(this.totalNotes / this.notesPerPage + 1)
                }
            }).catch(e => { console.log(e) })
        },
        addNote() {
            this.adding = 1
            setTimeout(() => {
                axios.post(URL + "addnote", { title: this.title, desc: this.desc }, { withCredentials: true }).catch(e => {
                    console.log(e)
                    this.error_message = e.response.data.message
                }).finally(e => {
                    this.getNotes()
                    this.adding = 0
                })
            }, 500)
        },
        updateNote(index) {
            this.updating = 1
            setTimeout(() => {
                const [title, desc, added] = this.notes[index]
                axios.put(URL + "updatenote", { title, desc, added }, { withCredentials: true }).catch(e => { console.log(e) }).finally(e => {
                    this.getNotes()
                    this.updating = 0
                    this.notes_updates[index] = false
                })
            }, 500)
        },
        deleteNote(index) {
            axios.delete(URL + `deletenote/${this.notes[index][2]}`, { withCredentials: true }).catch(e => { }).finally(e => {
                this.getNotes()
            })
        },
        changePage(page) {
            this.page = page
            this.getNotes()
            console.log(page)
            console.log(this.totalPages)
        }
    }))

    Alpine.data("footer", () => ({
        toggleTheme() {
            let theme = window.localStorage.getItem("theme")
            if (!theme) {
                theme = "dark"
            } else if (theme == "dark") {
                theme = "light"
            } else if (theme == "light") {
                theme = "dark"
            }
            window.localStorage.setItem("theme", theme)
            document.querySelector("html").setAttribute("data-theme", window.localStorage.getItem("theme"))
        },
        toggleLanguage() {
            let theme = window.localStorage.getItem("lan")
            if (!theme) {
                theme = "EN"
            } else if (theme == "EN") {
                theme = "PL"
            } else if (theme == "PL") {
                theme = "EN"
            }
            window.localStorage.setItem("lan", theme)
            Alpine.store("lan", theme)
            axios.defaults.baseURL = _URL + "/" + theme.toLowerCase()
            // () => {$store.lan == 'PL' ? $store.lan='EN' : $store.lan='PL'}
        }
    }))
})