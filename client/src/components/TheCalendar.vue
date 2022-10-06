<script>
import "@fullcalendar/core/vdom";
import FullCalendar from "@fullcalendar/vue3"
import dayGridPlugin from "@fullcalendar/daygrid"
import interactionPlugin from "@fullcalendar/interaction"

export default {
    components: {
        FullCalendar
    },
    props: {
        'dates': {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                dateClick: this.handleDateClick,
                //events: [{ title: 'event 1', date: '2022-10-08' },]
                events: this.dates
            }
        }
    },
    methods: {
        handleDateClick: function (arg) {
            alert('click ' + arg.dateStr)
        },
    }
}
</script>
    
<template>
    <FullCalendar :options="calendarOptions" />
</template>