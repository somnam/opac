import Field from '../widgets/field.js';
import Storage from '../storage.js';
import RadioList from '../widgets/radio_list.js';


class Activities extends Field {
    template = `
        <template>
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
        </template>
    `;

    constructor() {
        super();

        this.radioList = new RadioList('activities', 'activity');

        this.on('activities-show', () => this.onShow());

        this.on('activities-hide', () => this.remove());

        this.on('activities-results', () => this.emit('activities-show'));

        this.on('search-profile-show', () => this.emit('activities-hide'));

        this.on('in-progress-show', () => this.emit('activities-hide'));
    }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.radioList.update();
            })
            .catch(error => console.error(error));
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

        this.showLoading('#select-activity-btn');

        this.emit(`${activity.value}-request`);
    }

    backBtnListener(event) {
        event.preventDefault();

        Storage.remove('activity', 'activities');

        this.emit('activities-hide');
        this.emit('catalogs-show');
    }
}


export default Activities;
