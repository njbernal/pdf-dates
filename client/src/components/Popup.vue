<template>
    <div class="popup" :style="style">
        <div class="inner-container">
            <div class="close" @click="closePopup">
                <font-awesome-icon class="fa-2x close-button" :icon="['fas','circle-xmark']" />
            </div>
            <h3>File: {{props.data.filename}}</h3>
            <div class="blurb">{{props.data.blurb}}</div>
            <div class="pdf">
                <iframe v-if="pdfSwitch" class="pdf-container" :src="props.data.pdf"></iframe>
            </div>
            <div class="button-row">
                <div class="button" @click="activatePDF">{{pdfSwitch ? 'Hide PDF' : 'View PDF'}}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { watch, computed, ref, defineEmits } from 'vue'

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
});
const emit = defineEmits(['close-popup']);
const pdfSwitch = ref(false);

const style = computed(() => {
    const popup = document.getElementById('popup')
    let popupStyle = {}
    if (popup)
        popupStyle = popup.style

    let newStyle = {}
    if (props.data.active) {
        newStyle = {
            right: "calc(100% - " + (props.data.x - 220) + "px)",
            top: props.data.y + 'px',
            padding: "10px 20px",
            border: "1px solid var(--dark-blue)",
            borderRadius: "10px",
            opacity: 100,
        }
    } else {
        newStyle = {
            right: "calc(100% - " + (props.data.x - 220) + "px)",
            top: props.data.y + 'px',
            padding: "0",
            border: "none",
            borderRadius: "0",
            opacity: "0"
        }
    }
    return { ...popupStyle, ...newStyle };
})

const activatePDF = () => {
    pdfSwitch.value = pdfSwitch.value ? false : true
}

const closePopup = () => {
    emit('close-popup')
}
</script>
    

<style scoped>
h3 {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--magenta);
}

.blurb {
    font-size: 0.8em;
    white-space: nowrap;
    margin: 5px 0 10px 0;
}

.popup {
    position: absolute;
    width: auto;
    height: auto;
    opacity: 0;
    display: flex;
    flex-direction: column;
    background-color: #2f5a894a;
    z-index: 5;
    color: var(--blue-purple);
    font-size: 0.9rem;
    backdrop-filter: saturate(150%) blur(3px);
    -webkit-backdrop-filter: saturate(200%) blur(5px);
    transition: all 250ms ease;
}

.button-row {
    display: flex;
    justify-content: center;
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
    max-width: 50%;
    text-align: center;
}

.button:hover {
    background-color: var(--bright-blue);
}

.pdf-container {
    width: 100%;
    min-width: 600px;
    min-height: 800px;
    border: 1px solid var(--bright-blue);
    padding: 10px;
    border-radius: 10px;
}

.close {
    position: absolute;
    right: -25px;
    top: -15px;
    z-index: 6;
}

.close-button {
    color: var(--blue-purple);
    transition: all 250ms ease;
    cursor: pointer;
}

.close-button:hover {
    color: var(--bright-blue);
}

.inner-container {
    padding: 10px;
    border-radius: 10px;
    ;
}
</style>