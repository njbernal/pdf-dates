<script>
import "@fullcalendar/core/vdom";
import FullCalendar from "@fullcalendar/vue3"
import dayGridPlugin from "@fullcalendar/daygrid"
import interactionPlugin from "@fullcalendar/interaction"

export default {
    components: {
        FullCalendar
    },
    data() {
        return {
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth'
            }
        }
    }
}
</script>
    
<template>
    <FullCalendar :options="calendarOptions" />
</template>