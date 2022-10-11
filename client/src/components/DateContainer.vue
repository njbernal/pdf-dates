<template>
    <div :id="data.date" :style="{ backgroundColor: bg }" class="date-container" @mouseover="changeBackground" @mouseleave="resetBackground" @click="dateClicked">
        <div class="date-date">{{data.date}}</div>
        <div class="date-blurb">{{data.blurb}}</div>
    </div>
    <div class="file-divider-container">
        <div class="file-divider"></div>
    </div>
</template>

<script>
/*
This component represents a single date item listed in the file manager
*/
export default {
    name: "DateContainer",
    props: {
        data: {
            type: Object,
            required: true
        },
        color: {
            type: String,
            required: true
        }
    },
    emits: ['set-calendar-date', 'close-collapse'],
    data() {
        return {
            bg: ''
        }
    },
    methods: {
        dateClicked(e) {
            this.$emit('set-calendar-date', e.target.id)
            this.$emit('close-collapse')
        },
        changeBackground() {
            this.bg = this.color.substring(0, 7) + '11';
        },
        resetBackground() {
            this.bg = ''
        }
    }
}
</script>
            
<style scoped>
.date-container {
    cursor: pointer;
    padding: 5px;
    max-width: 400px;
    display: flex;
    color: var(--dark-blue);
    justify-content: flex-start;
}

.file-divider-container {
    display: flex;
    justify-content: center;
}

.file-divider {
    padding: 0;
    margin: 0;
    width: 90%;
    border-bottom: 1px solid var(--bright-blue-faded);
}

.date-date {
    margin: 0 10px 0 0;
    white-space: nowrap;
    font-size: 0.7em;
    font-weight: 500;
    color: var(--dark-blue);
}

.date-blurb {
    min-width: 300px;
    width: 300px;
    font-size: 0.7rem;
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--dark-blue);

}
</style>
        