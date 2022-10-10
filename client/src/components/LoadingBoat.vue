<template>
    <div id="welcome" :class="style" @click="hide">
        <img src="/images/harbour.gif" alt="Harbour loading" width="100" height="100" />
        <h2>Welcome, Harbour.</h2>
        <span>Click anywhere to begin.</span>
    </div>
</template>

<script setup>
import { computed } from 'vue'

/*
    Welcome page for Harbour!
*/

const props = defineProps({
    startingStyle: {
        type: String,
        required: true
    }
});

const style = computed(() => {
    console.log(props.startingStyle)
    return props.startingStyle
});

function hide() {
    // Hide the intro page
    document.getElementById('welcome').classList.add('fade');
    setTimeout(() => {
        document.getElementById('welcome').classList.remove('fullscreen');
    }, 1000);
}
</script>


<style scoped>
.fade {
    display: none;
    position: fixed;
    height: 0px;
    width: 0px;
    top: 0;
    left: 0;
    z-index: 0;
    opacity: 0;
    animation-name: fade;
    animation-duration: 1s;
    animation-iteration-count: 1;
}

@keyframes fade {
    from {
        opacity: 100%;
    }

    to {
        opacity: 0;
    }
}

.fullscreen {
    cursor: pointer;
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #fefefe77;
    z-index: 5;
    color: var(--blue-purple);
    font-size: 0.9rem;
    backdrop-filter: saturate(150%) blur(3px);
    -webkit-backdrop-filter: saturate(200%) blur(5px);
    transition: all 250ms ease;
}

.fullscreen>img {
    -webkit-filter: grayscale(0%);
    filter: grayscale(0%);
    transition: all 250ms ease;
    border-radius: 50px;
}

.fullscreen>img:hover {
    -webkit-filter: saturate(150%);
    filter: saturate(100%);
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    transform: rotate(15deg);
}


h2 {
    font-size: 2rem;
    margin: 10px 0 0 0;
    color: var(--dark-blue);
    letter-spacing: 1px;
}

span {
    font-style: italic;
    font-size: 0.8rem;
    color: var(--bright-blue);
    letter-spacing: 1px;
}
</style>