<template>
  <div
    class="jumbotron d-flex align-items-center"
    :style="{
      backgroundImage:
        'url(' + require('@/assets/images/home_page_banner.jpg') + ')',
      height: '500px',
      backgroundSize: cover,
    }"
  >
    <div class="container">
      <div
        class="text-white"
        :style="{ height: '100px', textShadow: '5px 5px 10px black' }"
      >
        <h1>Seamless Ticket Booking at Your Fingertips!</h1>
      </div>
      <button type="button" class="btn btn-primary btn-lg">Get Started</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>
