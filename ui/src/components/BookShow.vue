<template>
  <section class="vh-100">
    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <section class="jumbotron text-center">
            <div class="container">
              <h1 class="jumbotron-heading">Book Show Tickets</h1>
              <h4 class="jumbotron-heading">
                Secure Your Seat for an Unforgettable Movie Experience
              </h4>
              <img
                src="../assets/images/login_page.webp"
                class="img-fluid"
                alt="Sample image"
              />
            </div>
          </section>
        </div>

        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
          <form
            method="POST"
            id="register_user_form"
            @submit="bookShow"
            novalidate="true"
          >
            <h3 class="mb-3"></h3>
            <p class="mb-3">
              <i class="bi bi-geo-alt"></i> {{ theatreName }}, {{ theatreCity }}
            </p>
            <div class="p-3 mb-3 bg-light text-dark">
              <h5>{{ showName }}</h5>
            </div>
            <p class="mb-3">
              <i class="bi bi-calendar-week"></i> {{ formattedStartTime }}
            </p>
            <p class="mb-3"><i class="bi bi-clock-fill"></i> {{ duration }}</p>
            <div class="mb-3">
              <div v-if="errors.length" class="text-danger">
                <b>Please correct the following error(s):</b>
                <ul>
                  <li
                    v-for="error in errors"
                    v-bind:key="error"
                    class="text-danger"
                  >
                    {{ error }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label" for="available-seats"
                >Available seats</label
              >
              <input
                type="text"
                id="available-seats"
                class="form-control form-control-lg"
                name="available-seats"
                v-model="availableSeats"
                disabled
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="ticketCount"
                >Number of tickets</label
              >
              <input
                type="text"
                id="ticketCount"
                class="form-control form-control-lg"
                name="ticketCount"
                v-model="ticketCount"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label" for="price">Price</label>
              <input
                type="text"
                class="form-control form-control-lg"
                id="price"
                name="price"
                v-model="price"
                disabled
              />
            </div>
            <div class="mb-3">
              <label class="form-label" for="total">Total</label>
              <input
                type="number"
                class="form-control form-control-lg"
                id="total"
                name="total"
                v-model="total"
                disabled
              />
            </div>
            <div class="mb-3 d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg btn-block">
                Confirm Booking
                <span
                  v-if="showLoading"
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                >
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import moment from "moment";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "BookShow",
  data() {
    return {
      errors: [],
      theatreName: null,
      theatreCity: null,
      showName: null,
      startTime: null,
      endTime: null,
      availableSeats: null,
      ticketCount: null,
      price: null,
      total: null,
      showLoading: false,
    };
  },
  mounted() {
    this.fetchTheatreData();
    this.fetchShowData();
  },
  watch: {
    ticketCount(newVal) {
      this.total = this.price * newVal;
    },
  },
  computed: {
    formattedStartTime() {
      return moment(this.startTime, "YYYY-MM-DD HH:mm").format(
        "MMMM Do YYYY h:mm A"
      );
    },
    duration() {
      const start = moment(this.startTime, "YYYY-MM-DD HH:mm");
      const end = moment(this.endTime, "YYYY-MM-DD HH:mm");
      const duration = moment.duration(end.diff(start));
      var hours = parseInt(duration.asHours());
      var minutes = parseInt(duration.asMinutes()) % 60;
      return hours + " hours " + minutes + " minutes";
    },
  },
  methods: {
    async bookShow(e) {
      this.showLoading = true;
      e.preventDefault();
      this.errors = [];
      if (!this.ticketCount) {
        this.errors.push("Number of tickets required");
      }
      if (!this.errors.length) {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        const authTokenCookieValue = getCookie("authToken");
        headers.append("Authentication-Token", authTokenCookieValue);
        const request = new Request(
          "http://localhost:5000/api/" +
            localStorage.userid +
            "/theatre/" +
            localStorage.theatreId +
            "/show/" +
            localStorage.showId +
            "/booking",
          {
            method: "POST",
            body: JSON.stringify({
              count: this.ticketCount,
            }),
            headers: headers,
          }
        );
        await fetch(request)
          .then((response) => {
            if (response.status !== 201) {
              return response.json().then((errorData) => {
                // Extract error message from the response body
                const errorMessage =
                  errorData.message || "Unable to book tickets";
                throw new Error(errorMessage);
              });
            }
            return response.json();
          })
          .then(() => {
            this.$router.push({ name: "shows" });
          })
          .catch((error) => {
            this.errors.push(error.message);
          });
        this.showLoading = false;
      }
      this.showLoading = false;
    },
    async fetchTheatreData() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId,
        {
          method: "GET",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to fetch theatre";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.theatreName = data.name;
          this.theatreCity = data.city;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async fetchShowData() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId +
          "/show/" +
          localStorage.showId,
        {
          method: "GET",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage = errorData.message || "Unable to fetch show";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.showName = data.name;
          this.startTime = data.startTime;
          this.endTime = data.endTime;
          this.availableSeats = data.availableSeats;
          this.price = data.price;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
  },
};
</script>

<style scoped>
.h-custom {
  height: calc(100% - 73px);
}
@media (max-width: 450px) {
  .h-custom {
    height: 100%;
  }
}
</style>
