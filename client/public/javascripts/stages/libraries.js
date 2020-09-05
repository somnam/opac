import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import {RadioList, RadioListParams} from '../widgets/radio_list.js';


class Libraries {
    constructor() {
        this.radio_list = new RadioList('library-list-container', 'library');

        this.on('libraries-show', () => this.onLibrariesShow());

        this.on('libraries-hide', () => this.hide('#libraries-fields'));

        this.on('libraries-results', () => this.emit('libraries-show'));
    }

    onDomLoaded() {
        const backBtn = document.querySelector('#libraries-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const searchLibraryBtn = document.querySelector('#search-library-btn');
        searchLibraryBtn.addEventListener('click', (event) => {
            this.selectLibraryBtnListener(event);
        });
    }

    onLibrariesShow() {
        let librariesJson = this.storage.getItem('libraries');
        if (librariesJson !== null) {
            this.radio_list.update(new RadioListParams(
                JSON.parse(librariesJson),
                this.storage.getItem('library'),
            ));
        }

        this.show('#libraries-fields');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.storage.removeItem('library');
        this.storage.removeItem('libraries');

        this.emit('libraries-hide');
        this.emit('shelves-show');
    }

    selectLibraryBtnListener(event) {
        event.preventDefault();

        const value = document.querySelector('input[name="library"]:checked').value;

        const libraries = JSON.parse(this.storage.getItem('libraries'));

        const libraryIndex = libraries.findIndex((elem) => elem.value === value);

        const library = libraries[libraryIndex];

        this.storage.setItem('library', JSON.stringify(library));
    }
}


Object.assign(Libraries.prototype, EventEmitter);
Object.assign(Libraries.prototype, FieldMixin);

export default Libraries;
