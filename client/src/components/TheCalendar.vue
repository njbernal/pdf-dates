<script>
import Calendar from '@toast-ui/calendar'
import '@toast-ui/calendar/dist/toastui-calendar.min.css'

export default {
    props: {
        'dates': {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            calendar: '',
        }
    },
    watch: {
        dates() {
            this.updateCalendar()
        }
    },
    mounted() {
        this.createCalendar()
    },
    methods: {
        createCalendar: function () {
            this.calendar = new Calendar('#calendar', {
                defaultView: 'month',
                template: {
                    // allday(event) {
                    //     return `<span style="">${event.title}</span>`;
                    // },
                },
            });
            this.updateCalendar();
        },
        updateCalendar: function () {
            const keys = Object.keys(this.dates)
            const cals = []
            for (let filename of keys) {
                cals.push({
                    id: filename,
                    name: filename,
                    backgroundColor: '#' + Math.floor(Math.random() * 16777215).toString(16),
                });

                const dates = this.dates[filename].results
                const events = []
                for (let page in dates) {
                    for (let index in dates[page]) {
                        let obj = {
                            id: index,
                            calendarId: filename,
                            title: dates[page][index][1],
                            category: 'allday',
                            start: dates[page][index][0],
                            end: dates[page][index][0]
                        }
                        events.push(obj)
                    }
                }
                this.calendar.createEvents(events)
            }
            this.calendar.setCalendars(cals)
        }
    },
}
</script>
    
<template>
    <!-- <FullCalendar :options="calendarOptions" /> -->
    <div id="calendar"></div>
</template>

<style scoped>
#calendar {
    height: 600px;
    width: 600px;
}
</style>