<template>
    <div 
        :id="data.date" 
        :style="{ backgroundColor: bg }" 
        class="date-container" 
        @mouseover="changeBackground" 
        @mouseleave="resetBackground" 
        @click="dateClicked"
    >
        <div class="date-date">{{data.date}}</div>
        <div class="date-blurb">{{data.blurb}}</div>
        <div class="close" @click="closePopup">
            <font-awesome-icon 
                class="fa-1x close-button" 
                :icon="['fas','circle-xmark']" 
                :index="index" 
                :filename="filename" 
                @click="removeDate"
            />
        </div>
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
        filename: {
            type: String,
            required: true
        },
        color: {
            type: String,
            required: true
        },
        index: {
            type: Number,
            required: true
        }
    },
    emits: ['set-calendar-date', 'close-collapse', 'remove-date'],
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
        },
        removeDate() {
            this.$emit('remove-date', {
                index: this.index, 
                filename:this.filename
            });
        }
    }
}
</script>
            
<style scoped>
.date-container {
    cursor: pointer;
    padding: 5px;
    width: 100%;
    max-width: 100%;
    display: flex;
    color: var(--dark-blue);
    justify-content: space-between;
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
    max-width: 10%;
    color: var(--dark-blue);
}

.date-blurb {    
    max-width: 80%;
    font-size: 0.7rem;
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--dark-blue);
}
.close {
    max-width: 10%;
    z-index: 2;
}
.close-button {
    transition: all 250ms ease;
}
.close-button:hover {
    color: var(--bright-blue);
}
</style>
        