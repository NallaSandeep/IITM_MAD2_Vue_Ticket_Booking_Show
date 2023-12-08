<template>
  <main role="main">
    <section class="jumbotron text-center">
      <div class="container">
        <h2 class="jumbotron-heading">Booking History</h2>
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
          <div class="col-md-6" v-if="pageCount > 1">
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
</template>

<script>
import BookingCard from "./BookingCard";
import PaginationComponent from "./PaginationComponent";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "BookingListPage",
  data() {
    return {
      bookings: [],
      errors: [],
      showLoading: false,
      totalBookingCount: 0,
      pageCount: 0,
      currentPage: 1,
      query: "",
      pageSize: 15,
    };
  },
  components: {
    "booking-card": BookingCard,
    pagination: PaginationComponent,
  },
  mounted() {
    this.fetchBookingList();
    this.fetchBookingCount();
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
  },
  methods: {
    async fetchBookingList() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
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
    async fetchBookingCount() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
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
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchBookingList();
    },
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
