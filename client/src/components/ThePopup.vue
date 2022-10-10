<template>
    <div id="popup" class="hidden">
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
import { ref, defineEmits, onMounted } from 'vue'

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
});
const emit = defineEmits(['close-popup']);
const pdfSwitch = ref(false);

onMounted(() => {
    const popup = document.getElementById('popup')
    popup.classList.remove('hidden')
    popup.classList.add('popup')
    window.onkeydown = function (e) {
        if (e.keyCode === 27) {
            if (popup?.classList?.contains('popup'))
                closePopup()
            window.onkeydown = function (e) { }
        }
    };
})

const activatePDF = () => {
    pdfSwitch.value = pdfSwitch.value ? false : true
    const popup = document.getElementById('popup')
    popup.classList.toggle('active')
}

const closePopup = () => {
    const popup = document.getElementById('popup')
    popup.classList.remove('active')
    popup.classList.add('hidden')
    setTimeout(() => emit('close-popup'), "350");
}
</script>
    

<style scoped>
h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--magenta);
}

.blurb {
    font-size: 0.9em;
    white-space: nowrap;
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
    height: 130px;
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
    text-overflow: ellipsis;
    overflow: hidden;
}

.button-row {
    display: flex;
    justify-content: center;
}

.button {
    display: inline-block;
    padding: 10px 30px;
    margin: 5px 5px;
    cursor: pointer;
    border-radius: 5px;
    background-color: var(--dark-blue);
    font-size: 0.7rem;
    font-weight: bold;
    color: var(--vt-c-white-soft);
    transition: all 250ms ease;
    max-width: 50%;
    text-align: center;
}

.button:hover {
    background-color: var(--bright-blue);
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
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