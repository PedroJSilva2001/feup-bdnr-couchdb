<script>
	import { goto } from '$app/navigation';
	let reasonCode = '';
	let payerId = '';
	let coverage = [];
	let serverLoaded = false;
	let search = false;

	async function handlePayerCoverageSearch() {
		search = true;
		if (reasonCode && payerId) {
			let url = `http://localhost:8888/encounter-stats/payer-coverage?startkey=[${reasonCode}, "${payerId}"`;
			url += ']&endkey=[' + reasonCode + `, "${payerId}"`;
			url += ']';
			const response = await fetch(url);
			const data = await response.json();
			coverage = data.results;
			serverLoaded = true;
		} else {
			alert('Please enter a reason code and payer ID.');
		}
	}
</script>

<button
	class="route-button profile-button"
	on:click={() => {
		goto('/profile');
	}}
>
	My Profile
</button>
<button
	class="route-button logout-button"
	on:click={() => {
		localStorage.removeItem('ssn');
		localStorage.removeItem('pid');
		goto('/');
	}}
>
	Logout
</button>

<div class="container">
	<h1>Search Payer Coverage</h1>
	<div class="search-forms">
		<div class="search-form">
			<label for="reason-code">Reason Code:</label>
			<input id="reason-code" type="text" bind:value={reasonCode} placeholder="Reason Code" />
			<label for="payer-id">Payer ID:</label>
			<input id="payer-id" type="text" bind:value={payerId} placeholder="Payer ID" />
			<button on:click={handlePayerCoverageSearch}>Search</button>
		</div>
	</div>
	<div class="search-results">
		<h3>Results</h3>
		{#if !serverLoaded && search}
			<div class="loading">
				<h3><i class="fa fa-spinner fa-spin" /> Loading</h3>
			</div>
		{:else if Object.keys(coverage).length > 0 && serverLoaded}
			{#each coverage as result}
				<div class="card">
					<p><strong>Total Amount:</strong> {result.value}</p>
				</div>
			{/each}
		{:else}
			<div class="card">
				<p>No results found.</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.search-forms {
		display: flex;
		flex-direction: row;
		justify-content: center;
	}

	.search-form {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 1rem;
		margin-right: 1rem;
	}

	.search-form input {
		margin-bottom: 0.5rem;
	}

	.search-results {
		width: 100%;
	}
	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.fa-spinner {
		font-size: 2rem;
	}
	h3 {
		font-size: 2rem;
	}
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.route-button {
		position: absolute;
		top: 20px;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 10%;
		color: white;
		padding: 1rem 2rem;
		text-align: center;
		font-size: 1rem;
		cursor: pointer;
	}

	.profile-button {
		right: 10rem;
	}
	.logout-button {
		right: 1rem;
	}
</style>
