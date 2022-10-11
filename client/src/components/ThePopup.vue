<template>
    <div id="popup" ref="popup" class="hidden">
        <div id="innerPopup" class="inner-container">
            <div class="close" @click="closePopup">
                <font-awesome-icon class="fa-2x close-button" :icon="['fas','circle-xmark']" />
            </div>
            <div class="popup-info">
                <h3>{{props.data.filename}}</h3>
                <div class="blurb">{{props.data.blurb}}</div>
                <div v-if="pdfSwitch" class="pdf">
                    <iframe class="pdf-container" :src="props.data.pdf"></iframe>
                </div>
                <div class="button-row">
                    <div class="button" @click="activatePDF">{{pdfSwitch ? 'Hide PDF' : 'View PDF'}}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

/*
    Popup component for displaying details of an event in the calendar, and related PDF.
*/

const emit = defineEmits(['close-popup']);
const props = defineProps({
    data: {
        type: Object,
        required: true
    }
});

const pdfSwitch = ref(false)
const popup = ref()

onMounted(() => {
    // Setup the popup style and listen for 'esc' key.
    popup.value.classList.remove('hidden')
    popup.value.classList.add('popup')
    window.onkeydown = function (e) {
        if (e.keyCode === 27) {
            if (popup.value?.classList?.contains('popup'))
                closePopup()
            window.onkeydown = function () { }
        }
    };
})

const activatePDF = () => {
    // Open related PDF inside popup.
    pdfSwitch.value = pdfSwitch.value ? false : true
    popup.value.classList.toggle('active')
}

const closePopup = () => {
    // Close the popup.
    popup.value.classList.remove('active')
    popup.value.classList.add('hidden')
    setTimeout(() => emit('close-popup'), "350")
}
</script>
    

<style scoped>
h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--magenta);
}

.blurb {
    font-style: italic;
    width: 100%;
    font-size: 0.9em;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    margin: 5px 0 10px 0;
}

.hidden {
    opacity: 0;
    display: none;
}

.popup {
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #2f5a898a;
    z-index: 5;
    color: var(--blue-purple);
    font-size: 0.9rem;
    backdrop-filter: saturate(150%) blur(3px);
    -webkit-backdrop-filter: saturate(200%) blur(5px);
    transition: all 350ms ease;
    animation-name: popupFade;
    animation-duration: 300ms;
}

@keyframes popupFade {
    from {
        opacity: 0;
    }

    to {
        opacity: 100%;
    }
}

.inner-container {
    background-color: var(--vt-c-white-soft);
    height: 150px;
    width: 350px;
    max-width: 80%;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    transition: all 350ms ease;
}

.active>.inner-container {
    height: 90%;
    width: 100%;
}

.pdf {
    opacity: 0;
    transition: all 350ms ease;
}

.active>.inner-container>.popup-info {
    height: 100%;
}

.active>.inner-container>.popup-info>.pdf {
    height: 100%;
    opacity: 100%;
    animation-name: fadein;
    animation-duration: 1s;
}
@keyframes fadein {
    from {
        opacity: 0;
        height: 0%;
    }

    to {
        opacity: 100%;
        height: 100%
    }
}

.active>.inner-container>.popup-info>.pdf>.pdf-container {
    width: 100%;
    height: 100%;
    border: 1px solid var(--bright-blue);
    padding: 10px;
    border-radius: 10px;
}

.popup-info {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    width: 100%;
    padding: 5px;
}

.button-row {
    display: flex;
    justify-content: center;
}

.close {
    position: absolute;
    right: -7px;
    top: -7px;
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
</style>