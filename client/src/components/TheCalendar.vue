<script>
import Calendar from '@toast-ui/calendar'
import '@toast-ui/calendar/dist/toastui-calendar.min.css'

export default {
    props: {
        'dates': {
            type: Object,
            required: true
        },
        'startDate': {
            type: String,
            required: true
        },
        'colors': {
            type: Object,
            required: true
        }
    },
    emits: ['clickEvent', 'change-start-date'],
    data() {
        return {
            initialDate: false,
            calendar: '',
            displayMonth: '',
            displayYear: '',
            openDate: this.startDate,
            months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        }
    },
    watch: {
        dates() {
            this.updateCalendar()
        },
        startDate() {
            if (this.startDate)
                this.calendar.setDate(this.startDate)
            this.updateDisplay()
        }
    },
    mounted() {
        this.createCalendar()
    },
    methods: {
        createCalendar: function () {
            this.calendar = new Calendar('#calendar', {
                defaultView: 'month',
                useDetailPopup: false,
                useCreatePopup: false,
                gridSelection: false,
                isReadOnly: true
            });
            this.calendar.on({
                'clickEvent': (e) => {
                    const x = e.nativeEvent.clientX; //possibly pageX?>
                    const y = e.nativeEvent.clientY;
                    const filename = e.event.title;
                    const blurb = e.event.body;
                    const active = true;
                    this.$emit('clickEvent', { x, y, filename, blurb, active });
                },
            });
            this.updateCalendar();
            this.updateDisplay()
        },
        updateCalendar: function () {
            const keys = Object.keys(this.dates)
            const cals = []
            for (let filename of keys) {
                cals.push({
                    id: filename,
                    name: filename,
                    backgroundColor: this.colors[filename]
                });

                const dates = this.dates[filename].results
                const events = []
                for (let index in dates) {
                    if (!this.initialDate) {
                        this.calendar.setDate(dates[index].date)
                        this.initialDate = true
                        this.updateDisplay()
                    }
                    let obj = {
                        id: index,
                        calendarId: filename,
                        title: filename,
                        body: dates[index].blurb,
                        category: 'allday',
                        start: dates[index].date,
                        end: dates[index].date
                    }
                    events.push(obj)
                }
                this.calendar.createEvents(events)
            }
            this.calendar.setCalendars(cals)
        },
        updateDisplay: function () {
            const calDate = this.calendar.getDate()
            this.displayMonth = this.months[calDate.getMonth()]
            this.displayYear = calDate.getFullYear()
            this.$emit('change-start-date', { calDate })
        },
        calendarControl: function (e) {
            if (e.target.id === 'btn-today') {
                this.calendar.today()
            } else if (e.target.id === 'btn-prev') {
                this.calendar.prev()
            } else if (e.target.id === 'btn-next') {
                this.calendar.next()
            }
            this.updateDisplay()
        },
    },
}
</script>
    
<template>
    <div class="calendar-controls">
        <div class="calendar-controls-btns">
            <div id="btn-today" class="button" @click="calendarControl">Today</div>
            <div id="btn-prev" class="button" @click="calendarControl">Prev</div>
            <div id="btn-next" class="button" @click="calendarControl">Next</div>
        </div>
        <h3>{{displayMonth}} {{displayYear}}</h3>
    </div>

    <div class="calendar-container">
        <div id="calendar"></div>
    </div>
</template>

<style scoped>
.calendar-controls {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px 0;
    max-width: 800px;
}


.calendar-container {
    display: flex;
    justify-content: center;
}

#calendar {
    height: 400px;
    width: 100vw;
    font-size: 0.6em;
}

h3 {
    font-size: 1rem;
    font-weight: 400;
    color: var(--dark-blue);
    margin: 0 10px 0 0;
}


.button {
    display: inline-block;
    padding: 3px 20px;
    margin: 5px 5px;
    cursor: pointer;
    border-radius: 5px;
    background-color: var(--dark-blue);
    font-size: 0.7rem;
    font-weight: bold;
    color: var(--vt-c-white-soft);
    transition: all 250ms ease;
}

.button:hover {
    background-color: var(--bright-blue);
}

@media (min-width: 1024px) {
    h3 {
        font-size: 1.3rem;
        font-weight: 400;
        color: var(--dark-blue);
        margin: 0 10px 0 0;
    }

    .calendar-controls {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
        max-width: 800px;
        margin: 10px 0;
    }

    #calendar {
        height: 700px;
        width: 800px;
        font-size: 0.6em;
    }

    .button {
        display: inline-block;
        padding: 3px 20px;
        margin: 5px 5px;
        cursor: pointer;
        border-radius: 5px;
        background-color: var(--dark-blue);
        font-size: 0.8rem;
        font-weight: bold;
        color: var(--vt-c-white-soft);
        transition: all 250ms ease;
    }
}
</style>