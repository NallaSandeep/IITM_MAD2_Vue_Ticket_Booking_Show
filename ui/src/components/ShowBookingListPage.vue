<template>
  <div id="show-booking-listing">
    <toaster-message
      v-if="toasterVariant"
      :title="toasterVariant"
      :message="toasterMessage"
      :removeToast="clearToasterMessage"
    />
    <main role="main">
      <section class="jumbotron text-center">
        <div class="container">
          <h2 class="jumbotron-heading">
            <i class="bi bi-film"></i> {{ showName }}
          </h2>
          <p>
            <i class="bi bi-geo-alt"></i> {{ theatreName }}, {{ theatreArea }},
            {{ theatreCity }}
          </p>
          <p><i class="bi bi-clock-fill"></i> {{ formattedStartTime }}</p>
        </div>
      </section>
      <div class="album py-4 bg-light">
        <div class="container">
          <div class="row">
            <div class="col-md-6 mb-3">
              <input
                type="text"
                class="form-control"
                placeholder="Search..."
                v-model="query"
              />
            </div>
            <div class="col-md-2 d-flex align-items-start justify-content-end">
              <button
                class="btn btn-primary"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Export Show bookings Data"
                @click="exportShowBookingsData"
              >
                <i class="bi bi-box-arrow-down"></i> Export
              </button>
            </div>
            <div class="col-md-4" v-if="pageCount > 1">
              <pagination
                :currentPage="currentPage"
                :pageCount="pageCount"
                @page-changed="handlePageChange"
              />
            </div>
          </div>
          <div class="row" v-if="totalBookingCount === 0">
            <p>No Bookings available</p>
          </div>
          <div class="row" v-else>
            <booking-card
              v-for="(booking, index) in filteredBookings"
              :key="index"
              :userId="booking.userId"
              :theatreId="booking.theatreId"
              :theatreName="booking.theatreName"
              :theatreArea="booking.theatreArea"
              :theatreCity="booking.theatreCity"
              :showName="booking.showName"
              :showStartTime="booking.showStartTime"
              :showPrice="booking.showPrice"
              :bookingCount="booking.count"
              :bookedOn="booking.bookedOn"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import ShowBookingCard from "./ShowBookingCard";
import PaginationComponent from "./PaginationComponent";
import ToasterMessage from "./ToasterMessage";
import { getCookie } from "../util/cookie-util.js";
import moment from "moment";
export default {
  name: "ShowBookingListPage",
  data() {
    return {
      bookings: [],
      errors: [],
      showLoading: false,
      totalBookingCount: 0,
      pageCount: 0,
      currentPage: 1,
      query: "",
      pageSize: 20,
      toasterMessage: "",
      toasterVariant: "",
      timeoutId: null,
      showName: "",
      theatreName: "",
      theatreArea: "",
      theatreCity: "",
      showStartTime: "",
    };
  },
  components: {
    "booking-card": ShowBookingCard,
    pagination: PaginationComponent,
    "toaster-message": ToasterMessage,
  },
  mounted() {
    this.fetchTheatreData();
    this.fetchShowData();
    this.fetchShowBookingList();
    this.fetchShowBookingCount();
  },
  computed: {
    filteredBookings() {
      return this.bookings.filter(
        (booking) =>
          booking.theatreName
            .toLowerCase()
            .includes(this.query.toLowerCase()) ||
          booking.theatreCity
            .toLowerCase()
            .includes(this.query.toLowerCase()) ||
          booking.showName.toLowerCase().includes(this.query.toLowerCase()) ||
          booking.theatreArea.toLowerCase().includes(this.query.toLowerCase())
      );
    },
    formattedStartTime() {
      return this.showStartTime == null
        ? null
        : moment(this.showStartTime, "YYYY-MM-DD HH:mm").format(
            "MMMM Do YYYY h:mm A"
          );
    },
  },
  methods: {
    async fetchShowBookingList() {
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
          localStorage.showId +
          "/bookings?page=" +
          this.currentPage +
          "&size=" +
          this.pageSize,
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
                errorData.message || "Unable to fetch bookings";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.bookings = data;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async fetchShowBookingCount() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      // api/22/theatre/34/show/22/bookings
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId +
          "/show/" +
          localStorage.showId +
          "/bookings/pages?size=" +
          this.pageSize,
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
                errorData.message || "Unable to fetch booking count";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.totalBookingCount = data.itemCount;
          this.pageCount = data.pageCount;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
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
          this.theatreArea = data.theatreArea;
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
          this.showStartTime = data.startTime;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async exportShowBookingsData() {
      const headers = new Headers();
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId +
          "/show/" +
          localStorage.showId +
          "/bookings/report",
        {
          method: "POST",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to generate report";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.toasterVariant = "Success";
          this.toasterMessage = data.message;
          this.timeoutToaster();
        })
        .catch(() => {
          this.toasterVariant = "Failure";
          this.toasterMessage = "Unable to export the report";
        });
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchBookingList();
    },
    clearToasterMessage() {
      this.toasterVariant = "";
      this.toasterMessage = "";
      this.timeoutToaster();
    },
    timeoutToaster() {
      if (this.toasterMessage !== "" && this.toasterVariant !== "") {
        this.timeoutId = setTimeout(() => {
          this.clearToasterMessage();
        }, 5000);
      } else {
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
        }
      }
    },
  },
  beforeUnmount() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  },
};
</script>

<style>
:root {
  --jumbotron-padding-y: 1rem;
}

.jumbotron {
  padding-top: var(--jumbotron-padding-y);
  padding-bottom: var(--jumbotron-padding-y);
  margin-bottom: 0;
  background-color: #fff;
}

.jumbotron p:last-child {
  margin-bottom: 0;
}

.jumbotron-heading {
  font-weight: 300;
}

.jumbotron .container {
  max-width: 40rem;
}

.box-shadow {
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.05);
}
</style>
