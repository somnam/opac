import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from './widgets/radio_list.js';
import LoadingBtn from './widgets/loading_btn.js';


class Activities extends Field {
    template = `
      <fieldset id="activities-fields">
        <div id="activity-list-container" class="nes-container with-title mb-4">
          <h3 class="title">Activity</h3>
          <div class="item" id="activity-list">
          </div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="select-activity-btn">
          Next
        </button>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    items = [
        {"name": "Latest books", "value": "search-latest-books"},
        {"name": "Search books", "value": "search-books"},
    ];

    constructor(transport) {
        super();

        this.transport = transport;

        Storage.setEncoded('activities', {"items": this.items});

        this.radioList = new RadioList('activities', 'activity');

        this.loadingBtn = new LoadingBtn('#select-activity-btn');

        this.on('activities-show', () => this.onShow());

        this.on('activities-hide', () => this.remove());

        this.on('activities-next', () => this.onNext());

        this.on('activities-back', () => {
            this.emit('activities-hide');
            this.emit('catalogs-show');
        });
    }

    static toString() { return 'activities' }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.radioList.update();
            })
            .catch(error => console.error(error));
    }

    onNext() {
        const activity = Storage.getDecoded('activity');

        switch(activity ? activity.value : null) {
            case 'search-books':
                this.emit('activities-hide');
                this.emit('search-profile-show');
                break;
            case 'search-latest-books':
                this.emit('search-latest-books-start');
                break;
            default:
                console.error("Activity not defined.");
                break;
        }
    }

    addEvents() {
        const searchActivityBtn = document.querySelector('#select-activity-btn');
        searchActivityBtn.addEventListener('click', (event) => {
            this.selectActivityBtnListener(event);
        });

        const backBtn = document.querySelector('#activities-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    selectActivityBtnListener(event) {
        event.preventDefault();

        const activity = this.radioList.checked;

        Storage.setEncoded('activity', activity);

        this.loadingBtn.show();

        this.emit('activities-next');
    }

    backBtnListener(event) {
        event.preventDefault();

        Storage.remove('activity');

        this.emit('activities-back');
    }
}


export default Activities;
