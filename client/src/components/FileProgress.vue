<template>
    <div class="wrapper">
        <h3>LOADING...</h3>
    </div>
</template>

<style scope>
.wrapper {
    color: var(--dark-blue);
    padding: 3px 3px;
    text-align: center;
    font-size: 0.5em;
    letter-spacing: 2px;
    width: 100%;
    height: 100%;
    /* const colors = ['#5B9DDA33', '#DAA55B33', '#9D5BFA33', '#7CDA5B33', '#5B60DA33', '#DA5B5B33', '#D0DA5B33', '#C15BDA33'] */
    background: linear-gradient(45deg, #5B9DDA33, #DAA55B33, #9D5BFA33, #7CDA5B33, #5B60DA33, #DA5B5B33);
    background-size: 400% 400%;
    -webkit-animation: loadingGradient 1s ease infinite;
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
