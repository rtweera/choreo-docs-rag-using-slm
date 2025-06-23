# 7B
**Question:**  How can I set up Choreo to automatically deploy my microservice whenever I merge a pull request to a specific branch in my GitHub repository?
**Answer:** Based on the provided context, Choreo does not directly support automatic deployment triggered by GitHub pull requests or merges out of the box. However, you can enable `Auto Build on Commit` which will trigger a build for each commit pushed to your repository, and then configure `Auto Deploy on Build` to automatically deploy the built image.

Here's how you could set it up:

1. **Enable Auto Build on Commit**:
   - Go to the Build page.
   - Enable `Auto Build on Commit`. This will ensure that a build is triggered every time a commit is pushed, including when a pull request is merged into the specified branch.

2. **Enable Auto Deploy on Build**:
   - In the Deploy page, go to the Set Up card and enable `Auto Deploy on Build`.
   - This setting will automatically initiate deployment upon the completion of an automatic build.

By following these steps, you can ensure that your microservice is built and deployed every time a pull request is merged into the specified branch. However, this setup assumes that Choreo is configured to monitor your GitHub repository for push events and trigger builds accordingly. If your specific use case requires more granular control or integration with GitHub webhooks, you may need additional configuration steps not covered in the provided context.

For detailed instructions on integrating with GitHub webhooks directly, you might refer to additional documentation or support resources provided by Choreo.