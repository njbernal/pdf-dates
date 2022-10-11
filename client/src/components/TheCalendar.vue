<script>
import Calendar from '@toast-ui/calendar'
import '@toast-ui/calendar/dist/toastui-calendar.min.css'

/*
    Calendar component using TOAST UI's calendar.
    Used Vue3 options interface here for learning and demo purposes.
*/

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
        // Created the calendar when this component loads.
        this.createCalendar()
    },
    methods: {
        createCalendar: function () {
            // Initializes a new calendar.
            this.calendar = new Calendar('#calendar', {
                defaultView: 'month',
                useDetailPopup: false,
                useCreatePopup: false,
                gridSelection: false,
                isReadOnly: true
            });
            this.calendar.on({
                'clickEvent': (e) => {
                    const x = e.nativeEvent.clientX
                    const y = e.nativeEvent.clientY
                    const filename = e.event.title
                    const blurb = e.event.body
                    const active = true
                    this.$emit('clickEvent', { x, y, filename, blurb, active })
                },
            });
            this.updateCalendar()
            this.updateDisplay()
        },
        updateCalendar: function () {
            // Updates the calendar with new events
            this.calendar.clear()
            const keys = Object.keys(this.dates)
            const cals = []

            for (let filename of keys) {
                // Create the calendars
                cals.push({
                    id: filename,
                    name: filename,
                    backgroundColor: this.colors[filename]
                });
                
                const dates = this.dates[filename].results
                const events = []
                for (let index in dates) {
                    // Add events to calendar
                    if (!this.initialDate) {
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
                // Add the events
                this.calendar.createEvents(events)
            }
            // Add the calendars
            this.calendar.setCalendars(cals)
        },
        updateDisplay: function () {
            // Show the Month and Year the calendar is currently set to.
            const calDate = this.calendar.getDate()
            this.displayMonth = this.months[calDate.getMonth()]
            this.displayYear = calDate.getFullYear()
            this.$emit('change-start-date', { calDate })
        },
        calendarControl: function (e) {
            // Calendar control buttons.
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
}


.calendar-container {
    display: flex;
    justify-content: center;
}

#calendar {
    height: 450px;
    width: 95vw;
    font-size: 0.6em;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

h3 {
    font-size: 1rem;
    font-weight: 400;
    color: var(--dark-blue);
    margin: 0 10px 0 0;
}


.button {
    padding: 3px 20px;
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
        padding: 3px 20px;
    }

}
</style>