<template>
    <div class="wrapper">
        <span>Loading: </span>
        <span class="filename-container">
            <span v-for="(file, index) in props.filenames" :key="index" class="filenames">&nbsp;{{file.name}}&nbsp;</span>
        </span>
    </div>
</template>

<script setup>
/* 
    This component simply display a loading bar to inform the user the the server is
    processing the uploaded PDFs.
*/
const props = defineProps({
    filenames: {
        type: Object,
        required: true
    }
})
</script>

<style scope>
span {
    display: inline-block;
    white-space: nowrap;

}
.filename-container {
    max-width: 100%;
    padding: 5px;
    text-overflow: ellipsis;
    overflow: hidden;
}
.filenames {

}

.wrapper {
    max-width: 400px;
    color: var(--dark-blue);
    padding: 3px 3px;
    text-align: left;
    font-size: 0.7em;
    font-style: italic;
    letter-spacing: 1px;
    width: 100%;
    padding: 10px;
    height: 25px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    text-overflow: ellipsis;
    /* const colors = ['#5B9DDA33', '#DAA55B33', '#9D5BFA33', '#7CDA5B33', '#5B60DA33', '#DA5B5B33', '#D0DA5B33', '#C15BDA33'] */
    background: linear-gradient(45deg, #2F878933, #00aeff44, #2f5a8933, #2f5a8933, #2F878955, #00aeff44);
    background-size: 400% 400%;
    -webkit-animation: loadingGradient 3s ease infinite;
    -moz-animation: loadingGradient 3s ease infinite;
    animation: loadingGradient 3s ease infinite;
}

@-webkit-keyframes loadingGradient {
    0% {
        background-position: 0% 72%
    }

    50% {
        background-position: 100% 29%
    }

    100% {
        background-position: 0% 72%
    }
}

@-moz-keyframes loadingGradient {
    0% {
        background-position: 0% 72%
    }

    50% {
        background-position: 100% 29%
    }

    100% {
        background-position: 0% 72%
    }
}

@keyframes loadingGradient {
    0% {
        background-position: 0% 72%
    }

    50% {
        background-position: 100% 29%
    }

    100% {
        background-position: 0% 72%
    }
}
</style>
