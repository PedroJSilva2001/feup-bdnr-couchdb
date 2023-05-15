<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	let ssn;
	let condition = '';
	let startdate = '';
	let enddate = '';
	let evolution = [];
	let serverLoaded = false;
	let search = false;

	onMount(async () => {
		ssn = localStorage.getItem('ssn');
	});

	async function handlePatientEvolutionSearch() {
		search = true;
		if (condition) {
			let url = `http://localhost:8888/encounter-stats/patient-evolution?startkey=["${ssn}",${condition}`;
			if (startdate) {
				url += `, "${startdate}"`;
				if (enddate) {
					url += `, "${enddate}"`;
				}
			}
			url += `]&endkey=["${ssn}",${condition}`;
			if (startdate) {
				url += `, "${startdate}"`;
				if (enddate) {
					url += `, "${enddate}"`;
				}
			}
			url += ']';
			const response = await fetch(url);
			const data = await response.json();
			evolution = data.results;
			serverLoaded = true;
		} else {
			alert('Please enter a condition.');
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
	<h1>Search Patient Evolution</h1>
	<div class="search-forms">
		<div class="search-form">
			<label for="condition">Condition:</label>
			<input id="condition" type="text" bind:value={condition} placeholder="Condition" />
			<label for="startdate">Start Date:</label>
			<input id="startdate" type="date" bind:value={startdate} />
			<label for="enddate">End Date:</label>
			<input id="enddate" type="date" bind:value={enddate} />
			<button on:click={handlePatientEvolutionSearch}>Search</button>
		</div>
	</div>
	<div class="search-results">
		<h3>Results</h3>
		{#if !serverLoaded && search}
			<div class="loading">
				<h3><i class="fa fa-spinner fa-spin" /> Loading</h3>
			</div>
		{:else if Object.keys(evolution).length > 0 && serverLoaded}
			{#each evolution as result}
				<div class="card">
					<p><strong>Condition:</strong> {result.value.description}</p>
					<p><strong>Number of times w/ condition:</strong> {result.value.count}</p>
					<p><strong>Start Date:</strong> {result.value.earliest}</p>
					<p><strong>End Date:</strong> {result.value.latest}</p>
					<p><strong>Total days w/ condition:</strong> {result.value.incidenceDuration}</p>
					<p>
						<strong>Max nº of consecutive days w/ condition:</strong>
						{result.value.maxIncidenceDuration}
					</p>
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
