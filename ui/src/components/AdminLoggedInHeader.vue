<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">MyShow</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="/threatres">Theatres</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/shows">Shows</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/bookings">History</a>
          </li>
          <li class="nav-item">
            <a @click="logout" class="nav-link" href="#">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { deleteCookie } from "./../util/cookie-util.js";
import { mapMutations } from "vuex";
export default {
  name: "AdminLoggedInHeader",
  methods: {
    ...mapMutations(["setIsLoggedIn"]),
    async logout() {
      deleteCookie("authToken");
      this.setIsLoggedIn(false);
      this.$router.push({ name: "login" });
    },
  },
};
</script>
