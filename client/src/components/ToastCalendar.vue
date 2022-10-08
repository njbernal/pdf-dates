<template>
    <calendar style="height: 800px;" ref="tuiCalendar" :schedules="scheduleList" :useCreationPopup="useCreationPopup" @beforeCreateSchedule="onBeforeCreateSchedule" />
</template>

<script>
// import "../lib/tui-calendar/dist/tui-calendar.css";
import Calendar from '@toast-ui/calendar'
import '@toast-ui/calendar/dist/toastui-calendar.min.css'

export default {
    name: "myCalendar",
    components: {
        calendar: new Calendar
    },
    mounted() {
    },
    data() {
        return {
            dialog: false,
            useCreationPopup: false,
            useDetailPopup: true,
            count: 1,
            schedule: null,
            showMenu: false,
            x: 0,
            y: 0
        };
    },
    methods: {
        onCreateSchedule(value) {
            // add title and create schedule
            this.schedule[0].title = value;
            this.$refs.tuiCalendar.invoke("createSchedules", this.schedule);
        },
        onBeforeCreateSchedule(e) {
            // open custom popup
            var guide = e.guide;
            var guideEl$ = guide.guideElement
                ? guide.guideElement
                : guide.guideElements[Object.keys(guide.guideElements)[0]];
            this.x = guideEl$.getBoundingClientRect().left;
            this.y = guideEl$.getBoundingClientRect().top;
            this.showMenu = true;

            // schedule info
            var startTime = e.start;
            var endTime = e.end;
            var isAllDay = e.isAllDay;
            var schedule;

            this.schedule = [
                {
                    id: this.count++,
                    isAllDay: isAllDay,
                    start: startTime,
                    end: endTime,
                    category: "allday",
                    color: "#009eff",
                    bgColor: "#e9f6fb",
                    borderColor: "#009eff"
                }
            ];
            guide.clearGuideElement();
        },
    }
};
</script>