<template>
    <div id="welcome" :class="style" @click="hide">
        <img src="https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=100&amp;height=100&amp;name=ezgif.com-gif-maker.gif" alt="Harbour loading" width="100" height="100"
            loading="lazy" style="width: 100px;"
            srcset="https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=100&amp;height=100&amp;name=ezgif.com-gif-maker.gif 20w, https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=40&amp;height=40&amp;name=ezgif.com-gif-maker.gif 40w, https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=60&amp;height=60&amp;name=ezgif.com-gif-maker.gif 60w, https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=80&amp;height=80&amp;name=ezgif.com-gif-maker.gif 80w, https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=100&amp;height=100&amp;name=ezgif.com-gif-maker.gif 100w, https://www.harbourshare.com/hs-fs/hubfs/ezgif.com-gif-maker.gif?width=120&amp;height=120&amp;name=ezgif.com-gif-maker.gif 120w"
            sizes="(max-width: 100px) 100vw, 100px" />
        <h2>Welcome, Harbour.</h2>
        <span>Click anywhere to begin.</span>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    startingStyle: {
        type: String,
        required: true
    }
});

const style = computed(() => {
    return props.startingStyle
});

function hide() {
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
    background-color: #fefefe22;
    z-index: 5;
    color: var(--blue-purple);
    font-size: 0.9rem;
    backdrop-filter: saturate(150%) blur(3px);
    -webkit-backdrop-filter: saturate(200%) blur(5px);
    transition: all 350ms ease;
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